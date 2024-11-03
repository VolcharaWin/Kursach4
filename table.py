import sys
import psycopg2
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Создаем виджет для таблицы
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        # Подключаемся к базе данных и загружаем данные
        self.load_data()

    def load_data(self):
        # Настройте параметры подключения к вашей базе данных
        conn = psycopg2.connect(
            database = "Gostinitsa",
            user = "1",
            password = "1",
            host = "localhost",
            port = "5432"
        )

        # Выполняем запрос для получения данных
        cur = conn.cursor()
        cur.execute("SELECT * FROM clienti")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        # Настраиваем таблицу
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(colnames))
        self.table_widget.setHorizontalHeaderLabels(colnames)

        # Заполняем таблицу данными
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # Закрываем соединение с базой данных
        cur.close()
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec())
