import sys
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem, QTableView, QTableWidget

from util_funcs import add_everything, show_everything

class AddProjivWindow(QWidget):
    window_closed = pyqtSignal()
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление проживающего")

        self.add_number = QLabel("id")
        self.add_fio = QLabel("ФИО")
        self.add_bd = QLabel("День рождения")
        self.add_pass = QLabel("Серия и номер")
        self.add_zas = QLabel("Номер заселения")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_projiv)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.add_number_line = QLineEdit(self)
        self.add_fio_line = QLineEdit(self)
        self.add_bd_line = QLineEdit(self)
        self.add_pass_line = QLineEdit(self)
        self.add_zas_line = QLineEdit(self)

        self.table_projiv = QTableWidget(self)
        # Расположение формы заполнения через сетку
        form_layout = QGridLayout()
        form_layout.addWidget(self.add_number, 0, 0)
        form_layout.addWidget(self.add_number_line, 0, 1)

        form_layout.addWidget(self.add_fio, 1, 0)
        form_layout.addWidget(self.add_fio_line, 1, 1)

        form_layout.addWidget(self.add_bd, 2, 0)
        form_layout.addWidget(self.add_bd_line, 2, 1)

        form_layout.addWidget(self.add_pass, 3, 0)
        form_layout.addWidget(self.add_pass_line, 3, 1)

        form_layout.addWidget(self.add_zas, 4, 0)
        form_layout.addWidget(self.add_zas_line, 4, 1)

        # Расположение для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_projiv)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_projiv()
    def add_projiv(self):
        input_fields = {
            'projid': self.add_number_line,
            'projfio': self.add_fio_line,
            'projbd': self.add_bd_line,
            'projpass': self.add_pass_line,
            'zasid': self.add_zas_line
        }
        insert_query = """
            INSERT INTO projiv (projid, projfio, projbd, projpass, zasid)
            VALUES (%s, %s, %s, %s, %s)            
        """
        add_everything(
            self=self,
            connection=self.connection,
            input_fields=input_fields,
            sql_query=insert_query,
            success_message="Проживающий был успешно добавлен!",
            error_message="Ошибка при добавлении проживающего!"
        )
        self.show_projiv()
    def show_projiv(self):
        show_query = "SELECT * FROM projiv ORDER BY projiv ASC"
        show_everything(
            self=self,
            connection=self.connection,
            table_widget=self.table_projiv,
            sql_query=show_query
        )
    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication()

    window = AddProjivWindow()

    window.show()

    sys.exit(app.exec())