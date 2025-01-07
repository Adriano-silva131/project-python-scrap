from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt


class PaginationWidget(QWidget):
    def __init__(self, total_pages, current_page, on_page_change):
        super().__init__()
        self.total_pages = total_pages
        self.current_page = current_page
        self.on_page_change = on_page_change

        self.layout = QHBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.update_buttons()

    def update_buttons(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        first_button = QPushButton("<<")
        first_button.setEnabled(self.current_page > 0)
        first_button.clicked.connect(lambda: self.on_page_change(0))
        self.layout.addWidget(first_button)

        prev_button = QPushButton("<")
        prev_button.setEnabled(self.current_page > 0)
        prev_button.clicked.connect(lambda: self.on_page_change(self.current_page - 1))
        self.layout.addWidget(prev_button)

        for i in range(
            max(0, self.current_page - 2), min(self.total_pages, self.current_page + 3)
        ):
            page_button = QPushButton(str(i + 1))
            page_button.setCheckable(True)
            page_button.setChecked(i == self.current_page)
            page_button.clicked.connect(lambda checked, page=i: self.change_page(page))
            self.layout.addWidget(page_button)

        next_button = QPushButton(">")
        next_button.setEnabled(self.current_page < self.total_pages - 1)
        next_button.clicked.connect(lambda: self.change_page(self.current_page + 1))
        self.layout.addWidget(next_button)

        last_button = QPushButton(">>")
        last_button.setEnabled(self.current_page < self.total_pages - 1)
        last_button.clicked.connect(lambda: self.change_page(self.total_pages - 1))
        self.layout.addWidget(last_button)

    def change_page(self, page):
        self.current_page = page
        self.update_buttons()
        self.on_page_change(page)

    def set_data(self, total_pages, current_page):
        self.total_pages = total_pages
        self.current_page = current_page
        self.update_buttons()
