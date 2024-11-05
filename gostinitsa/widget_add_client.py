import sys, psycopg2
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem, QTableView, QTableWidget


class add_client_window(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

        #self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Добавление клиента')
        self.add_number = QLabel(self)
        self.add_number.setText('id клиента')

        self.add_fio = QLabel(self)
        self.add_fio.setText('ФИО клиента')

        self.add_bd = QLabel(self)
        self.add_bd.setText('День рождения клиента')

        self.add_pass = QLabel(self)
        self.add_pass.setText('Паспорт клиента')

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_client)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.update_button = QPushButton("Обновить таблицу")
        self.update_button.clicked.connect(self.show_clients)

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
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.add_button)

        #Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_clients)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_clients()
    def show_clients(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM clienti ORDER BY clientid ASC")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]

            self.table_clients.setRowCount(len(rows))
            self.table_clients.setColumnCount(len(colnames))
            self.table_clients.setHorizontalHeaderLabels(colnames)

            self.table_clients.verticalHeader().setVisible(False)
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.table_clients.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при выводе клиентов: {e}")
            cursor.close()
            self.connection.rollback()
    def add_client(self):
        client_id = self.add_number_line.text()
        client_fio = self.add_fio_line.text()
        client_bd = self.add_bd_line.text()
        client_pass = self.add_pass_line.text()

        if not all([client_id, client_bd, client_pass, client_fio]):
            QMessageBox.critical(self, "Ошибка", "Заполните все поля")
            return
        try:
            cursor = self.connection.cursor()
            insert_query = """
                INSERT INTO clienti (clientid, clientfio, clientbd, clientpass)
                VALUES (%s, %s, %s, %s)            
            """
            cursor.execute(insert_query, (client_id, client_fio, client_bd, client_pass))
            self.connection.commit()
            cursor.close()
            QMessageBox.information(self, "Успех", "Клиент был успешно добавлен")
            print("Данные успешно добавлены в базу данных!")
        except(Exception, psycopg2.Error) as error:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении клиента: {error}")
            print("Ошибка при добавлении клиента в базу данных: ", error)
            self.connection.rollback()
        # Очистка полей после записи
        client_id = self.add_number_line.clear()
        client_fio = self.add_fio_line.clear()
        client_bd = self.add_bd_line.clear()
        client_pass = self.add_pass_line.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = add_client_window()
    myApp.show()
    sys.exit(app.exec())

