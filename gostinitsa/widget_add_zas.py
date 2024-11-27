import sys
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, \
    QGridLayout, QPushButton, QHBoxLayout, QTableWidget

from util_funcs import add_everything, show_everything

class AddZasWindow(QWidget):
    window_closed = pyqtSignal()
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление заселения")

        self.add_number = QLabel("id")
        self.add_datein= QLabel("Дата заселения")
        self.add_dateout = QLabel("Дата выселения")
        self.add_puslid = QLabel("Номер предоставления")
        self.add_clientid = QLabel("Номер клиента")
        self.add_nomid = QLabel("Номер номера")
        self.add_persid = QLabel("Номер персонала")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_zas)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)

        self.add_number_line = QLineEdit(self)
        self.add_datein_line = QLineEdit(self)
        self.add_dateout_line = QLineEdit(self)
        self.add_puslid_line = QLineEdit(self)
        self.add_clientid_line = QLineEdit(self)
        self.add_nomid_line = QLineEdit(self)
        self.add_persid_line = QLineEdit(self)

        self.table_zas = QTableWidget(self)
        # Расположение формы заполнения через сетку
        form_layout = QGridLayout()
        form_layout.addWidget(self.add_number, 0, 0)
        form_layout.addWidget(self.add_number_line, 0, 1)

        form_layout.addWidget(self.add_datein, 1, 0)
        form_layout.addWidget(self.add_datein_line, 1, 1)

        form_layout.addWidget(self.add_dateout, 2, 0)
        form_layout.addWidget(self.add_dateout_line, 2, 1)

        form_layout.addWidget(self.add_puslid, 3, 0)
        form_layout.addWidget(self.add_puslid_line, 3, 1)

        form_layout.addWidget(self.add_clientid, 4, 0)
        form_layout.addWidget(self.add_clientid_line, 4, 1)

        form_layout.addWidget(self.add_nomid, 5, 0)
        form_layout.addWidget(self.add_nomid_line, 5, 1)

        form_layout.addWidget(self.add_persid, 6, 0)
        form_layout.addWidget(self.add_persid_line, 6, 1)


        # Расположение для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # Главный вертикальный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_zas)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(435, 400)
        self.show_zas()

    def add_zas(self):
        input_fields = {
            'zasid': self.add_number_line,
            'zasdatein': self.add_datein_line,
            'zasdateout': self.add_dateout_line,
            'puslid': self.add_puslid_line,
            'clientid': self.add_clientid_line,
            'nomid': self.add_nomid_line,
            'persid': self.add_persid_line
        }
        insert_query = """
            ALTER TABLE Zaselenie DISABLE TRIGGER ALL;
            INSERT INTO zaselenie (zasid, zasdatein, zasdateout, puslid, clientid, nomid, persid)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            ALTER TABLE Zaselenie ENABLE TRIGGER ALL;
        """
        add_everything(
            self=self,
            connection=self.connection,
            input_fields=input_fields,
            sql_query=insert_query,
            success_message="Дополнительная услуга был успешно добавлен!",
            error_message="Ошибка при добавлении дополнительной услуги!"
        )
        self.show_zas()

    def show_zas(self):
        show_query = "SELECT * FROM zaselenie ORDER BY zasid ASC"
        show_everything(
            self=self,
            connection=self.connection,
            table_widget=self.table_zas,
            sql_query=show_query
        )
    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication()

    window = AddZasWindow()

    window.show()

    sys.exit(app.exec())