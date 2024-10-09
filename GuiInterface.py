import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLineEdit, QWidget, QDialog, QLabel
from PyQt6.QtGui import QIcon
from config import SessionLocal
from models import Ordem
from models import Camada
from generate_pdf import generate_pdf

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dados da")
        self.setGeometry(100, 100, 800, 600)

        # Criar o QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)

        # Carregar os dados na tabela
        self.load_data()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.table_widget)

        # Central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def filter_table(self):
        search_text = self.search_bar.text().lower()

        for row in range(self.table_widget.rowCount()):
            ordem_item = self.table_widget.item(row, 0)  # Coluna 0 é a "Ordem"
            if ordem_item:
                ordem_text = ordem_item.text().lower()
                # Mostra/oculta a linha baseada na pesquisa
                self.table_widget.setRowHidden(row, search_text not in ordem_text)

    def load_data(self):
        # Criar uma sessão usando SessionLocal definida em settings
        session = SessionLocal()

        # Query com SQLAlchemy para buscar os dados da tabela ordens
        ordens = session.query(Ordem).all()

        # Preencher a tabela com os dados obtidos
        self.table_widget.setRowCount(len(ordens))
        for row_num, ordem in enumerate(ordens):
            self.table_widget.setItem(row_num, 0, QTableWidgetItem(ordem.ordem))
            self.table_widget.setItem(row_num, 1, QTableWidgetItem(str(ordem.numero_pecas)))
            self.table_widget.setItem(row_num, 2, QTableWidgetItem(ordem.product_type))
            self.table_widget.setItem(row_num, 3, QTableWidgetItem(ordem.nome_arquivo))

            # Criar um botão de extração para cada linha
            extract_button = QPushButton("Visualizar Dados")
            extract_button.setIcon(QIcon("src/pdf_icon.png"))  # Substitua pelo caminho correto do ícone
            extract_button.clicked.connect(lambda checked, row=row_num: self.extract_data(row))
            self.table_widget.setCellWidget(row_num, 4, extract_button)  # Coluna 4 para os botões
            
            self.table_widget.setItem(row_num, 5, QTableWidgetItem(str(ordem.id)))
            
            # Adicionar o botão de gerar PDF na última coluna
            pdf_button = QPushButton("Gerar PDF")
            pdf_button.setIcon(QIcon("src/gerar_pdf.png"))  # Substitua pelo caminho correto do ícone
            pdf_button.clicked.connect(lambda checked, ordem=ordem: self.generate_pdf(ordem))  # Passa a ordem para o método
            self.table_widget.setCellWidget(row_num, 6, pdf_button)
            # Passa o índice da linha para o método

    
    
            # Adicionar o botão na última coluna

        self.table_widget.setColumnHidden(5, True)

        # Barra de pesquisa (QLineEdit)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Pesquisar pela ordem...")
        self.search_bar.textChanged.connect(self.filter_table)  # Conecta o evento de texto mudado ao filtro

        # Definindo os cabeçalhos das colunas
        self.table_widget.setHorizontalHeaderLabels(["Ordem", "Número de Peças", "Tipo de Produto", "Nome Arquivo", ""])

        # Fechar a sessão
        session.close()

    def extract_data(self, row):
        
        ordem_id = self.table_widget.item(row,5).text()

        session = SessionLocal()
        
        camadas = session.query(Camada).filter_by(ordem_id=ordem_id).all()
        
        if camadas: 
            self.show_camadas(camadas)
            
        session.close()
    
    def show_camadas(self, camadas):
        # Criar um diálogo modal para exibir as camadas
        dialog = QDialog(self)
        dialog.setWindowTitle("Camadas Relacionadas")

        # Layout vertical para adicionar as informações das camadas
        layout = QVBoxLayout()

        # Percorrer todas as camadas e exibir as informações
        for camada in camadas:
            # Criar um rótulo (QLabel) para cada camada
            camada_label = QLabel(f"Camada: {camada.camada}, Tecido: {camada.tecido}, Quantidade Enfesto: {camada.quantidade_enfesto}")
            layout.addWidget(camada_label)

        # Configurar o layout no diálogo
        dialog.setLayout(layout)

        # Exibir o diálogo
        dialog.exec()
        
    def generate_pdf(self, ordem):
        session = SessionLocal()

        # Buscar camadas relacionadas à ordem
        camadas = session.query(Camada).filter_by(ordem_id=ordem.id).all()

        # Chamar a função do arquivo pdf_generator.py passando ordem e camadas
        generate_pdf(ordem, camadas, logo_path="src/cenciveste-removebg-preview.png")

        session.close()

# Inicializar a aplicação
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
