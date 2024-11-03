import sys, psycopg2
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QGridLayout, QPushButton, QHBoxLayout

class add_client_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавление клиента')
        self.add_number = QLabel(self)
        self.add_number.setText('id клиента')

        self.add_fio = QLabel(self)
        self.add_fio.setText('ФИО клиента')

        self.add_bd = QLabel(self)
        self.add_bd.setText('День рождения клиента')

        self.add_pass = QLabel(self)
        self.add_pass.setText('Паспорт клиента')

        self.add_button = QPushButton(self)
        self.add_button.setText('Добавить')
        #self.add_button.triggered.connect(self.add_client)

        self.back_button = QPushButton(self)
        self.back_button.setText('Назад')

        self.add_number_line = QLineEdit(self)
        self.add_fio_line = QLineEdit(self)
        self.add_bd_line = QLineEdit(self)
        self.add_pass_line = QLineEdit(self)

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
        button_layout.addStretch() # Заполнитель
        button_layout.addWidget(self.add_button)

        #Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(400, 300)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = add_client_window()
    myApp.show()
    sys.exit(app.exec())

