import sys, psycopg2
import csv
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QTableWidget,QMainWindow, QPushButton, \
    QMessageBox, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog

from widget_add_client import add_client_window
from login_window import LogInWindow

class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        query = "SELECT table_name \
                FROM information_schema.tables \
                WHERE table_schema = 'public';"

        self.connection = connection
        central_widget = QWidget()

        btn_check = QPushButton('Проверить')
        #btn_check.clicked.connect(lambda: self.get_table_names(query))
        btn_check.clicked.connect(self.display_all_fields)

        btn_add_all = QPushButton('Добавить всех клиентов')
        #btn_add_all.clicked.connect(self.open_csv_and_add_clients)

        btn_remove_all = QPushButton('Удалить всех клиентов')
        #btn_add_all.clicked.connect(self.remove_all_clients)


        test_layout = QVBoxLayout()
        test_layout.addWidget(btn_check, alignment=Qt.AlignmentFlag.AlignCenter)
        test_layout.addWidget(btn_add_all, alignment=Qt.AlignmentFlag.AlignCenter)
        test_layout.addWidget(btn_remove_all, alignment=Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(test_layout)
        self.setCentralWidget(central_widget)

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

        self.setFixedSize(600, 600)
    def open_add_client_window(self):
        self.client_window = add_client_window()
        self.client_window.show()

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос с использованием переданного соединения."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.fetchall()
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка выполнения запроса: {error}')
            return None

    def get_table_names(self, query, params=None):
        results = self.execute_query(query, params)
        if results is not None:
            for table in results:
                table_name = table[0]
                print(table_name)
    def display_all_fields(self):
        """Получает и отображает все поля из всех таблиц в базе данных."""
        try:
            # Получаем список всех таблиц
            query_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            tables = self.execute_query(query_tables)

            if tables:
                for table in tables:
                    table_name = table[0]  # Имя таблицы
                    print(table_name)

                    # Получаем столбцы для каждой таблицы
                    '''query_columns = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
                    columns = self.execute_query(query_columns, (table_name,))

                    if columns:
                        column_names = [col[0] for col in columns]  # Извлекаем имена столбцов
                        print("Columns:", column_names)
                    else:
                        print("No columns found.")'''
            else:
                print("No tables found.")
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при получении данных: {error}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LogInWindow()

    login_window.connection_successful.connect(lambda conn: setattr(login_window, 'main_window',
                                            MainWindow(conn)) or login_window.main_window.show())
    login_window.show()

    sys.exit(app.exec())