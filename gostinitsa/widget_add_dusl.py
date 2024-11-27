import sys
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QTableWidget

from util_funcs import add_everything, show_everything

class AddDuslWindow(QWidget):
    window_closed = pyqtSignal()
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление дополнительной услуги")

        self.add_number = QLabel("id")
        self.add_name = QLabel("Название")
        self.add_price= QLabel("Цена")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_dusl)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.add_number_line = QLineEdit(self)
        self.add_price_line = QLineEdit(self)
        self.add_name_line = QLineEdit(self)

        self.table_dusl = QTableWidget(self)
        # Расположение формы заполнения через сетку
        form_layout = QGridLayout()
        form_layout.addWidget(self.add_number, 0, 0)
        form_layout.addWidget(self.add_number_line, 0, 1)

        form_layout.addWidget(self.add_name, 1, 0)
        form_layout.addWidget(self.add_name_line, 1, 1)

        form_layout.addWidget(self.add_price, 2, 0)
        form_layout.addWidget(self.add_price_line, 2, 1)


        # Расположение для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_dusl)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_dusl()

        # Устанавливаем порядок переключения через Tab
        self.setTabOrder(self.add_number_line, self.add_name_line)
        self.setTabOrder(self.add_name_line, self.add_price_line)
        self.setTabOrder(self.add_price_line, self.add_button)
        self.setTabOrder(self.add_button, self.back_button)

    def add_dusl(self):
        input_fields = {
            'duslid': self.add_number_line,
            'duslname': self.add_name_line,
            'duslprice': self.add_price_line
        }
        insert_query = """
            INSERT INTO dopuslugi (duslid, duslname, duslprice)
            VALUES (%s, %s, %s)            
        """
        add_everything(
            self=self,
            connection=self.connection,
            input_fields=input_fields,
            sql_query=insert_query,
            success_message="Дополнительная услуга был успешно добавлен!",
            error_message="Ошибка при добавлении дополнительной услуги!"
        )
        self.show_dusl()
    def show_dusl(self):
        show_query = "SELECT * FROM dopuslugi ORDER BY duslid ASC"
        show_everything(
            self=self,
            connection=self.connection,
            table_widget=self.table_dusl,
            sql_query=show_query
        )
    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication()

    window = AddDuslWindow()

    window.show()

    sys.exit(app.exec())