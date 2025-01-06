import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QDialog,
    QLabel,
    QHBoxLayout,
    QFileDialog,
    QCheckBox,
    QMessageBox,
    QSpinBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from config import SessionLocal
from models import Ordem
from models import Camada
from generate_pdf import generate_pdf
from main import main


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dados da")
        self.setGeometry(100, 100, 800, 600)

        self.current_page = 0
        self.page_size = 50
        self.total_pages = 0

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setStyleSheet(
            """
            QTableWidget {
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                padding: 5px;
                text-align: left;
            }
        """
        )

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Pesquisar pela ordem...")
        self.search_bar.textChanged.connect(self.filter_table)

        self.update_button = QPushButton("Atualizar")
        self.update_button.clicked.connect(self.update_data)

        self.select_dir_button = QPushButton("Selecionar Diretório")
        self.select_dir_button.clicked.connect(self.select_directory)

        self.selected_dir_label = QLabel("Diretório selecionado:")

        self.prev_button = QPushButton("Anterior")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Próximo")
        self.next_button.clicked.connect(self.next_page)

        self.page_label = QLabel("Página:")
        self.page_spinbox = QSpinBox()
        self.page_spinbox.setMinimum(1)
        self.page_spinbox.valueChanged.connect(self.go_to_page)

        button_layout = QHBoxLayout()
        layout = QVBoxLayout()

        button_layout.addWidget(self.search_bar)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.select_dir_button)

        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        layout.addWidget(self.selected_dir_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()

    def filter_table(self):
        try:
            search_text = self.search_bar.text().lower()
            session = SessionLocal()

            query = session.query(Ordem).filter((Ordem.ordem.ilike(f"%{search_text}%")))

            total_items = query.count()
            self.total_pages = total_items + self.page_size - 1

            if total_items <= self.page_size:
                ordens = query.all()
                self.current_page = 0
            else:
                offset = self.current_page * self.page_size
                ordens = query.offset(offset).limit(self.page_size).all()

                offset = self.current_page * self.page_size
                ordens = query.offset(offset).limit(self.page_size).all()

            session.close()
            self.display_data(ordens)

            self.prev_button.setEnabled(self.current_page > 0)
            self.next_button.setEnabled(total_items > self.current_page and self.current_page < self.total_pages - 1)

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def load_data(self):
        session = SessionLocal()

        total_items = session.query(Ordem).count()
        self.total_pages = total_items + self.page_size - 1

        offset = self.current_page * self.page_size

        ordens = session.query(Ordem).offset(offset).limit(self.page_size).all()
        session.close()
        self.display_data(ordens)
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)
        self.page_label.setText(f"Página: {self.current_page + 1} / {self.total_pages}")

    def display_data(self, ordens):
        self.table_widget.setRowCount(len(ordens))

        for row_num, ordem in enumerate(ordens):
            self.table_widget.setItem(row_num, 0, QTableWidgetItem(ordem.ordem))
            self.table_widget.setItem(
                row_num, 1, QTableWidgetItem(str(ordem.numero_pecas))
            )
            self.table_widget.setItem(row_num, 2, QTableWidgetItem(ordem.product_type))
            self.table_widget.setItem(row_num, 3, QTableWidgetItem(ordem.nome_arquivo))

            extract_button = QPushButton("Visualizar Dados")
            extract_button.setIcon(QIcon("src/pdf_icon.png"))
            extract_button.clicked.connect(
                lambda checked, row=row_num: self.extract_data(row)
            )
            self.table_widget.setCellWidget(row_num, 4, extract_button)

            self.table_widget.setItem(row_num, 5, QTableWidgetItem(str(ordem.id)))

            pdf_button = QPushButton("Gerar PDF")
            pdf_button.setIcon(QIcon("src/gerar_pdf.png"))
            pdf_button.clicked.connect(
                lambda checked, ordem=ordem: self.generate_pdf(ordem)
            )
            self.table_widget.setCellWidget(row_num, 6, pdf_button)

        self.table_widget.setColumnHidden(5, True)
        self.table_widget.setHorizontalHeaderLabels(
            ["Ordem", "Número de Peças", "Tipo de Produto", "Nome Arquivo", "", ""]
        )

    def extract_data(self, row):
        try:
            ordem_id = self.table_widget.item(row, 5).text()
            session = SessionLocal()
            camadas = session.query(Camada).filter_by(ordem_id=ordem_id).all()
            ordem = session.query(Ordem).filter_by(id=ordem_id).first()

            if camadas and ordem:
                self.show_camadas(camadas, ordem)
            session.close()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def show_camadas(self, camadas, ordem):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Selecione as Camadas para Gerar PDF")

            layout = QVBoxLayout()

            checkboxes = []
            for camada in camadas:
                checkbox = QCheckBox(
                    f"Camada: {camada.camada}, Tecido: {camada.tecido}, Quantidade Enfesto: {camada.quantidade_enfesto}"
                )
                checkboxes.append((checkbox, camada))
                layout.addWidget(checkbox)

            generate_button = QPushButton("Gerar PDF")
            generate_button.clicked.connect(
                lambda: self.generate_pdf_selected_camadas(ordem, checkboxes, dialog)
            )
            layout.addWidget(generate_button)

            dialog.setLayout(layout)
            dialog.exec()
        except Exception as e:
            print(e)

    def generate_pdf_selected_camadas(self, ordem, checkboxes, dialog):
        selected_camadas = [
            camada for checkbox, camada in checkboxes if checkbox.isChecked()
        ]
        print(f"Camadas selecionadas: {[c.camada for c in selected_camadas]}")
        if selected_camadas:
            generate_pdf(
                ordem, selected_camadas, logo_path="src/cenciveste-removebg-preview.png"
            )
            dialog.accept()
        else:
            QMessageBox.warning(self, "Aviso", "Nenhuma camada foi selecionada!")

    def generate_pdf(self, ordem):
        session = SessionLocal()
        camadas = session.query(Camada).filter_by(ordem_id=ordem.id).all()
        generate_pdf(ordem, camadas, logo_path="src/cenciveste-removebg-preview.png")
        session.close()

    def update_data(self):
        main()
        self.load_data()

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecione o Diretório")
        if directory:
            self.selected_dir_label.setText(f"Diretório selecionado: {directory}")
            self.update_data(directory)

    def update_data(self, directory_path=None):
        if directory_path:
            main(directory_path)
        self.load_data()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        if self.search_bar.text():
            self.filter_table()
        else:
            self.load_data()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        if self.search_bar.text():
            self.filter_table()
        else:
            self.load_data()

    def go_to_page(self):
        selected_page = self.page_spinbox.value() - 1
        if 0 <= selected_page < self.total_pages:
            self.current_page = selected_page
            if self.search_bar.text():
                self.filter_table()
            else:
                self.load_data()


try:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
except Exception as e:
    print(f"Ocorreu um erro: {e}")
