import psycopg2
import sys
from PyQt6 import QtWidgets
from test import Ui_MainWindow  # Импортируем сгенерированный класс интерфейса

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_connections()
        self.connection = self.connect_to_database()
    def setup_connections(self):
        self.ui.add_client_push_button.clicked.connect(self.add_client)

    def connect_to_database(self):
        try:
            connection = psycopg2.connect(
                database="Gostinitsa",
                user="postgres",
                password="Werere3601308wer",
                host="localhost",
                port="5432"
            )
            print("Успешное подключение к базе данных!")
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Ошибка подключения к базе данных: ", error)
            return None

    def add_client(self):
        if self.connection is None:
            print("Нет соединения с базой данных")
            return

        client_id = self.ui.clientid_line.text()
        client_fio = self.ui.clientfio_line.text()
        client_bd = self.ui.clientbd_line.text()
        client_pass = self.ui.clientpass_line.text()

        if not all([client_id, client_bd, client_pass, client_fio]):
            blank_error = QtWidgets.QMessageBox(self)
            blank_error.setText("Заполните все поля!")
            blank_error.exec()
            print("Не все поля заполнены. Заполните все поля!")
            return
        """# Открываем файл для записи и записываем данные
        with open('data.txt', 'w', encoding='utf-8') as file:
            file.write(f"ID клиента: {client_id}\n")
            file.write(f"ФИО: {client_fio}\n")
            file.write(f"Дата рождения: {client_bd}\n")
            file.write(f"Серия и номер паспорта: {client_pass}\n")"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
                INSERT INTO clienti (clientid, clientfio, clientbd, clientpass)
                VALUES (%s, %s, %s, %s)            
            """
            cursor.execute(insert_query, (client_id, client_fio, client_bd, client_pass))
            self.connection.commit()
            cursor.close()
            print("Данные успешно добавлены в базу данных!")
        except(Exception, psycopg2.Error) as error:
            print("Ошибка при добавлении клиента в базу данных: ", error)
            self.connection.rollback()
        # Очистка полей после записи
        self.ui.clientid_line.clear()
        self.ui.clientfio_line.clear()
        self.ui.clientbd_line.clear()
        self.ui.clientpass_line.clear()
    def closeEvent(self, event):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")
            event.accept()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())