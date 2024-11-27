import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QTableWidget,QMainWindow, \
    QMessageBox, QGridLayout, QLabel, QVBoxLayout, QWidget, \
    QTableWidgetItem, QScrollArea, QSizePolicy, QHeaderView
from widget_add_client import AddClientWindow
from widget_add_projiv import AddProjivWindow
from widget_add_nomer import AddNomerWindow
from widget_add_dusl import AddDuslWindow
from widget_add_pusl import AddPuslWindow
from widget_add_zas import AddZasWindow
from widget_add_pers import AddPersWindow
from login_window import LogInWindow

def resource_path(relative_path):
    """ Получает путь к ресурсу для PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # Путь в режиме PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    # Путь при обычном запуске
    return os.path.join(os.path.abspath("."), relative_path)

# Добавляем класс TablesWidget
class TablesWidget(QWidget):
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.connection = connection

        container = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        layout = QGridLayout()
        container.setLayout(layout)

        tables_data = self.get_tables_data()

        num_tables = len(tables_data)
        row = 0
        col = 0

        # Отключаем растяжение колонок, чтобы таблицы могли занимать свою ширину
        # layout.setColumnStretch(0, 1)
        # layout.setColumnStretch(1, 1)

        for index, (table_name, headers, rows) in enumerate(tables_data):
            label = QLabel(f"Таблица: {table_name}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Создаем виджет таблицы
            table_widget = QTableWidget()
            table_widget.setRowCount(len(rows))
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Настраиваем режим изменения размера столбцов
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table_widget.horizontalHeader().setStretchLastSection(True)
            #table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Настраиваем политику размеров таблицы
            table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            # Заполняем таблицу данными
            for i, row_data in enumerate(rows):
                for j, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    table_widget.setItem(i, j, item)

            # Оборачиваем таблицу в собственную область прокрутки
            table_scroll_area = QScrollArea()
            table_scroll_area.setWidgetResizable(True)
            table_scroll_area.setWidget(table_widget)

            # Настраиваем политику прокрутки области прокрутки
            table_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

            # (Опционально) Устанавливаем максимальную высоту области прокрутки
            # table_scroll_area.setMaximumHeight(200)  # Закомментируйте или измените при необходимости

            # Контейнер для заголовка и области прокрутки таблицы
            table_container = QWidget()
            table_layout = QVBoxLayout()
            table_layout.addWidget(label)  # Добавляем заголовок
            table_layout.addWidget(table_scroll_area)  # Добавляем область прокрутки с таблицей
            table_container.setLayout(table_layout)

            # Настраиваем политику размеров для контейнера
            table_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            if num_tables % 2 == 1 and index == num_tables - 1:
                # Последняя таблица при нечетном количестве занимает два столбца
                layout.addWidget(table_container, row, 0, 1, 2)
            else:
                layout.addWidget(table_container, row, col)
                col += 1
                if col >= 2:  # Переходим на следующую строку, если столбцы заполнены
                    col = 0
                    row += 1

        # Если последний ряд заполнен только наполовину, увеличиваем номер ряда
        if col != 0:
            row += 1

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос с использованием переданного соединения."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка выполнения запроса: {error}')
            return None

    def get_tables_data(self):
        """Получает данные всех таблиц из базы данных."""
        try:
            # Получаем список всех таблиц
            query_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            tables = self.execute_query(query_tables)

            tables_data = []

            if tables:
                for table in tables:
                    table_name = table[0]  # Имя таблицы

                    # Получаем имена столбцов
                    query_columns = """
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position;
                    """
                    columns = self.execute_query(query_columns, (table_name,))

                    headers = [col[0] for col in columns] if columns else []

                    # Получаем данные таблицы
                    query_data = f"SELECT * FROM {table_name};"
                    rows = self.execute_query(query_data)

                    tables_data.append((table_name, headers, rows))
            else:
                QMessageBox.information(self, "Информация", "В базе данных нет таблиц.")

            return tables_data
        except Exception as error:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при получении данных: {error}')
            return []

class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        central_widget = QWidget()

        # Вместо self.table_widget используем TablesWidget
        self.tables_widget = TablesWidget(self.connection)

        '''Работа с расположением'''
        test_layout = QVBoxLayout()
        test_layout.addWidget(self.tables_widget)
        central_widget.setLayout(test_layout)
        self.setCentralWidget(central_widget)

        '''Работа с меню'''
        self.setWindowTitle('Гостиница')

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('Управление')

        add_client_action = QAction("Добавление клиента", self)
        add_client_action.triggered.connect(self.open_add_client_window)

        add_nomer_action = QAction("Добавление номера", self)
        add_nomer_action.triggered.connect(self.open_add_nomer_window)

        add_projiv_action = QAction("Добавление проживающего", self)
        add_projiv_action.triggered.connect(self.open_add_projiv_window)

        add_dusl_action = QAction("Добавление дополнительной услуги", self)
        add_dusl_action.triggered.connect(self.open_add_dusl_window)

        add_pusl_action = QAction("Добавление предоставления услуги", self)
        add_pusl_action.triggered.connect(self.open_add_pusl_window)

        add_zas_action = QAction("Добавление заселения", self)
        add_zas_action.triggered.connect(self.open_add_zas_window)

        add_pers_action = QAction("Добавление персонала", self)
        add_pers_action.triggered.connect(self.open_add_pers_window)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(add_client_action)
        file_menu.addAction(add_projiv_action)
        file_menu.addAction(add_nomer_action)
        file_menu.addAction(add_dusl_action)
        file_menu.addAction(add_pusl_action)
        file_menu.addAction(add_zas_action)
        file_menu.addAction(add_pers_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        self.csv_file_path = None

        self.setFixedSize(800, 600)  # Увеличил размер окна для лучшего отображения

        # Загрузка данных таблиц при запуске
        # self.load_databases_and_tables()

    def open_add_client_window(self):
        self.client_window = AddClientWindow(self.connection)
        self.client_window.window_closed.connect(self.refresh_tables)
        self.client_window.show()

    def open_add_projiv_window(self):
        self.projiv_window = AddProjivWindow(self.connection)
        self.projiv_window.window_closed.connect(self.refresh_tables)
        self.projiv_window.show()

    def open_add_nomer_window(self):
        self.nomer_window = AddNomerWindow(self.connection)
        self.nomer_window.window_closed.connect(self.refresh_tables)
        self.nomer_window.show()

    def open_add_dusl_window(self):
        self.dusl_window = AddDuslWindow(self.connection)
        self.dusl_window.window_closed.connect(self.refresh_tables)
        self.dusl_window.show()

    def open_add_pusl_window(self):
        self.pusl_window = AddPuslWindow(self.connection)
        self.pusl_window.window_closed.connect(self.refresh_tables)
        self.pusl_window.show()

    def open_add_zas_window(self):
        self.zas_window = AddZasWindow(self.connection)
        self.zas_window.window_closed.connect(self.refresh_tables)
        self.zas_window.show()

    def open_add_pers_window(self):
        self.pers_window = AddPersWindow(self.connection)
        self.pers_window.window_closed.connect(self.refresh_tables)
        self.pers_window.show()

    def refresh_tables(self):
        # Remove the old tables widget
        old_tables_widget = self.tables_widget
        self.tables_widget = TablesWidget(self.connection)
        # Replace the old widget with the new one in the layout
        self.centralWidget().layout().replaceWidget(old_tables_widget, self.tables_widget)
        old_tables_widget.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LogInWindow()
    app.setWindowIcon(QIcon(resource_path('icon.png')))
    with open(resource_path('style.qss'), 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    def open_main_window(conn):
        login_window.main_window = MainWindow(conn)
        login_window.main_window.show()
        login_window.close()  # Закрываем окно логина после успешного входа

    login_window.connection_successful.connect(open_main_window)
    login_window.show()

    sys.exit(app.exec())
