import sys
import math
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
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from config import SessionLocal
from models import Ordem
from models import Camada
from generate_pdf import generate_pdf
from main import main
from gui.PaginationWidget import PaginationWidget
from services.directory_save import save_directory, load_directory
from services.FolderWatcher import start_folder_watcher


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dados do risco de enfesto")
        self.setGeometry(100, 100, 800, 600)

        self.folder_observer = None
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
        self.update_button.clicked.connect(self.load_data)

        self.select_dir_button = QPushButton("Selecionar Diretório")
        self.select_dir_button.clicked.connect(self.select_directory)

        self.selected_dir_label = QLabel("Diretório selecionado:")

        button_layout = QHBoxLayout()
        layout = QVBoxLayout()

        button_layout.addWidget(self.search_bar)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.select_dir_button)

        layout.addWidget(self.selected_dir_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)

        self.pagination_widget = PaginationWidget(
            total_pages=self.total_pages,
            current_page=self.current_page,
            on_page_change=self.change_page,
        )
        layout.addWidget(self.pagination_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        saved_directory = load_directory()

        if saved_directory:
            self.selected_dir_label.setText(f"Diretório selecionado: {saved_directory}")
            self.start_watching_directory(saved_directory)
        else:
            self.selected_dir_label.setText("Nenhum diretório selecionado.")

        self.load_data()

    def filter_table(self):
        try:
            search_text = self.search_bar.text().lower()
            session = SessionLocal()

            query = session.query(Ordem).filter((Ordem.ordem.ilike(f"%{search_text}%")))

            total_items = query.count()

            self.total_pages = math.ceil(total_items / self.page_size)

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

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def start_watching_directory(self, directory):
        if self.folder_observer:
            self.folder_observer.stop()
        self.folder_observer = start_folder_watcher(directory)
        self.update_data()

    def load_data(self):
        session = SessionLocal()

        total_items = session.query(Ordem).count()
        self.total_pages = math.ceil(total_items / self.page_size)

        offset = self.current_page * self.page_size
        ordens = session.query(Ordem).offset(offset).limit(self.page_size).all()
        session.close()

        self.display_data(ordens)
        self.pagination_widget.set_data(self.total_pages, self.current_page)

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
        directory = (
            self.selected_dir_label.text()
            .replace("Diretório selecionado: ", "")
            .strip()
        )
        if directory:
            main(directory)  # Passe o caminho do diretório como argumento
            self.load_data()
        else:
            QMessageBox.warning(
                self, "Aviso", "Nenhum diretório selecionado para atualizar os dados!"
            )

    def select_directory(self):
        try:
            directory = QFileDialog.getExistingDirectory(self, "Selecione o Diretório")
            if directory:
                self.selected_dir_label.setText(f"Diretório selecionado: {directory}")
                save_directory(directory)

            if self.folder_observer:
                self.folder_observer.stop()

            self.folder_observer = start_folder_watcher(directory)
            main(directory)
            self.load_data()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

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

    def change_page(self, page):
        self.current_page = page
        self.load_data()


try:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
except Exception as e:
    print(f"Ocorreu um erro: {e}")
