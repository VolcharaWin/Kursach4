import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem, QTableView, QTableWidget

from util_funcs import add_everything, show_everything

class AddPuslWindow(QWidget):
    window_closed = pyqtSignal()
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление предоставления услуги")

        self.add_number = QLabel("id")
        self.add_avail = QLabel("Доступность")
        self.add_dusl = QLabel("Номер услуги")
        self.add_persid = QLabel("Номер персонала")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_pusl)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.add_number_line = QLineEdit(self)
        self.add_avail_line = QLineEdit(self)
        self.add_dusl_line = QLineEdit(self)
        self.add_persid_line = QLineEdit(self)

        self.table_pusl = QTableWidget(self)
        # Расположение формы заполнения через сетку
        form_layout = QGridLayout()
        form_layout.addWidget(self.add_number, 0, 0)
        form_layout.addWidget(self.add_number_line, 0, 1)

        form_layout.addWidget(self.add_avail, 1, 0)
        form_layout.addWidget(self.add_avail_line, 1, 1)

        form_layout.addWidget(self.add_dusl, 2, 0)
        form_layout.addWidget(self.add_dusl_line, 2, 1)

        form_layout.addWidget(self.add_persid, 3, 0)
        form_layout.addWidget(self.add_persid_line, 3, 1)

        # Расположение для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_pusl)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_pusl()
    def add_pusl(self):
        input_fields = {
            'puslid': self.add_number_line,
            'puslavail': self.add_avail_line,
            'duslid': self.add_dusl_line,
            'persid': self.add_persid_line
        }
        insert_query = """
            INSERT INTO preduslug (puslid, puslavail, duslid, persid)
            VALUES (%s, %s, %s, %s)            
        """
        add_everything(
            self=self,
            connection=self.connection,
            input_fields=input_fields,
            sql_query=insert_query,
            success_message="Предоставление услуги было успешно добавлен!",
            error_message="Ошибка при добавлении представления услуги!"
        )
        self.show_pusl()
    def show_pusl(self):
        show_query = "SELECT * FROM preduslug ORDER BY puslid ASC"
        show_everything(
            self=self,
            connection=self.connection,
            table_widget=self.table_pusl,
            sql_query=show_query
        )

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication()

    window = AddPuslWindow()

    window.show()

    sys.exit(app.exec())