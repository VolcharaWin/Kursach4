import sys
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QTableWidget

from util_funcs import add_everything, show_everything

class AddNomerWindow(QWidget):
    window_closed = pyqtSignal()
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление номера")

        self.add_number = QLabel("id")
        self.add_price= QLabel("Цена за сутки")
        self.add_mesta = QLabel("Количество мест")
        self.add_persid = QLabel("Номер сотрудника")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_nomer)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.add_number_line = QLineEdit(self)
        self.add_price_line = QLineEdit(self)
        self.add_mesta_line = QLineEdit(self)
        self.add_persid_line = QLineEdit(self)

        self.table_nomer = QTableWidget(self)
        # Расположение формы заполнения через сетку
        form_layout = QGridLayout()
        form_layout.addWidget(self.add_number, 0, 0)
        form_layout.addWidget(self.add_number_line, 0, 1)

        form_layout.addWidget(self.add_price, 1, 0)
        form_layout.addWidget(self.add_price_line, 1, 1)

        form_layout.addWidget(self.add_mesta, 2, 0)
        form_layout.addWidget(self.add_mesta_line, 2, 1)

        form_layout.addWidget(self.add_persid, 3, 0)
        form_layout.addWidget(self.add_persid_line, 3, 1)

        # Расположение для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_nomer)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_nomer()
    def add_nomer(self):
        input_fields = {
            'nomid': self.add_number_line,
            'nomprice': self.add_price_line,
            'nommesta': self.add_mesta_line,
            'persid': self.add_persid_line
        }
        insert_query = """
            INSERT INTO nomera (nomid, nomprice, nommesta, persid)
            VALUES (%s, %s, %s, %s)            
        """
        add_everything(
            self=self,
            connection=self.connection,
            input_fields=input_fields,
            sql_query=insert_query,
            success_message="Номер был успешно добавлен!",
            error_message="Ошибка при добавлении номера!"
        )
        self.show_nomer()
    def show_nomer(self):
        show_query = "SELECT * FROM nomera ORDER BY nomid ASC"
        show_everything(
            self=self,
            connection=self.connection,
            table_widget=self.table_nomer,
            sql_query=show_query
        )
    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication()

    window = AddNomerWindow()

    window.show()

    sys.exit(app.exec())