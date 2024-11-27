import sys
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QTableWidget
from util_funcs import add_everything, show_everything


class AddClientWindow(QWidget):
    window_closed = pyqtSignal()
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        #self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Добавление клиента')
        self.add_number = QLabel(self)
        self.add_number.setText('id')

        self.add_fio = QLabel(self)
        self.add_fio.setText('ФИО клиента')

        self.add_bd = QLabel(self)
        self.add_bd.setText('День рождения клиента')

        self.add_pass = QLabel(self)
        self.add_pass.setText('Серия и номер')

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_client)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.add_number_line = QLineEdit(self)
        self.add_fio_line = QLineEdit(self)
        self.add_bd_line = QLineEdit(self)
        self.add_pass_line = QLineEdit(self)


        self.table_clients = QTableWidget(self)
        #Расположение формы заполнения через сетку
        form_layout = QGridLayout()
        form_layout.addWidget(self.add_number, 0, 0)
        form_layout.addWidget(self.add_number_line, 0, 1)

        form_layout.addWidget(self.add_fio, 1, 0)
        form_layout.addWidget(self.add_fio_line, 1, 1)

        form_layout.addWidget(self.add_bd, 2, 0)
        form_layout.addWidget(self.add_bd_line, 2, 1)

        form_layout.addWidget(self.add_pass, 3, 0)
        form_layout.addWidget(self.add_pass_line, 3, 1)

        #Расположение для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment = QtCore.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.add_button, alignment = QtCore.Qt.AlignmentFlag.AlignRight)

        #Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_clients)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_clients()
    def show_clients(self):
        show_query = "SELECT * FROM clienti ORDER BY clientid ASC"
        show_everything(
            self=self,
            connection=self.connection,
            table_widget=self.table_clients,
            sql_query=show_query
        )
    def add_client(self):
        input_fields = {
            'clientid': self.add_number_line,
            'clientfio': self.add_fio_line,
            'clientbd': self.add_bd_line,
            'clientpass': self.add_pass_line
        }
        insert_query = """
                INSERT INTO clienti (clientid, clientfio, clientbd, clientpass)
                VALUES (%s, %s, %s, %s)            
            """
        add_everything(
            self=self,
            connection=self.connection,
            input_fields=input_fields,
            sql_query=insert_query,
            success_message="Клиент был успешно добавлен!",
            error_message="Ошибка при добавлении клиента!"
        )
        self.show_clients()
    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = AddClientWindow()
    myApp.show()
    sys.exit(app.exec())

