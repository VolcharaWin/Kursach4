import sys, psycopg2
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QWidget, QLineEdit, QVBoxLayout, QMessageBox, QGridLayout

DATABASE = "Gostinitsa"
USER = '1'
HOST = "localhost"
PORT = "5432"
class LogInWindow(QWidget):
    connection_successful = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        central_widget = QWidget(self)
        self.setWindowTitle('Подключение')

        db_name_label = QLabel(f'Подключение к базе данных {DATABASE}')

        btn_connect = QPushButton('Подключиться')
        btn_connect.setAutoDefault(True)

        user_label = QLabel()
        user_label.setText('Пользователь: ')

        password_label = QLabel()
        password_label.setText('Пароль: ')

        self.user_line = QLineEdit()
        self.user_line.returnPressed.connect(btn_connect.click)
        self.password_line = QLineEdit()
        self.password_line.returnPressed.connect(btn_connect.click)
        self.password_line.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout = QGridLayout()
        form_layout.addWidget(user_label, 0, 0)
        form_layout.setAlignment(user_label, Qt.AlignmentFlag.AlignRight)

        form_layout.addWidget(self.user_line, 0, 1)
        form_layout.setAlignment(self.user_line, Qt.AlignmentFlag.AlignLeft)

        form_layout.addWidget(password_label, 1, 0)
        form_layout.setAlignment(password_label, Qt.AlignmentFlag.AlignRight)

        form_layout.addWidget(self.password_line, 1, 1)
        form_layout.setAlignment(self.password_line, Qt.AlignmentFlag.AlignLeft)

        main_layout = QVBoxLayout()
        main_layout.addWidget(db_name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(btn_connect, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        self.setFixedSize(300, 200)
        btn_connect.clicked.connect(self.connect_to_database)
    def connect_to_database(self):
        user = self.user_line.text()
        password = self.password_line.text()

        if not all([user, password]):
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля')
            return None
        try:
            connection = psycopg2.connect(
                database=DATABASE,
                user=user,
                password=password,
                host=HOST,
                port=PORT
            )
            #QMessageBox.information(self, 'Успех', f'Успешное подключение к базе данных')
            print("Успешное подключение к базе данных")

            self.connection_successful.emit(connection)
            self.close()
            return connection
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка подключения к базе данных{error}')
            print(f"Ошибка подключения к базе данных: {error}")
            return None