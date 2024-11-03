import sys, psycopg2
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QGridLayout, QLabel, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QWidget

from widget_add_client import add_client_window

DATABASE = "Gostinitsa"
HOST = "localhost"
PORT = "5432"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        '''Работа с меню'''
        self.setWindowTitle('гостиница')

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('Управление')
        help_menu = menu_bar.addMenu('Help')

        open_action = QAction("Добавление клиента", self)
        open_action.triggered.connect(self.open_add_client_window)
        save_action = QAction("Добавление заселения", self)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)

        about_action = QAction("Action", self)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu.addAction(about_action)


        '''Работа с главным окном'''
        #self.connect = self.connect_to_database()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

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

        central_widget.setLayout(main_layout)

        self.setFixedSize(300, 200)

        btn_connect.clicked.connect(self.connect_to_database)
    def open_add_client_window(self):
        self.client_window = add_client_window()
        self.client_window.show()

    def connect_to_database(self):
        user = self.user_line.text()
        password = self.password_line.text()

        if not all([user, password]):
            self.blank_error_box()
            return None
        try:
            connection = psycopg2.connect(
                database=DATABASE,
                user=user,
                password=password,
                host=HOST,
                port=PORT
            )
            self.success_box  = QMessageBox(self)
            self.success_box.setWindowTitle('Успех')
            self.success_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.success_box.setText(f'Успешное подключение к базе данных {DATABASE}')
            self.success_box.exec()
            print("Успешное подключение к базе данных!")
            return connection
        except (Exception, psycopg2.Error) as error:
            self.error_box = QMessageBox(self)
            self.error_box.setIcon(QMessageBox.Icon.Warning)
            self.error_box.setWindowTitle('Ошибка')
            self.error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.error_box.setText(f"Ошибка подключения к базе данных: {error}")
            self.error_box.exec()
            print("Ошибка подключения к базе данных: ", error)
            return None

    def blank_error_box(self):
        blank_error = QMessageBox(self)
        blank_error.setText("Заполните все поля!")
        blank_error.setStandardButtons(QMessageBox.StandardButton.Ok)
        blank_error.exec()

    def closeEvent(self, event):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")
            event.accept()
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())