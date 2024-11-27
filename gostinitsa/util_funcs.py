# Универсальный функции для оптимизации кода при обращении к базе данных
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
import psycopg2


def add_everything(self, connection, input_fields, sql_query, success_message, error_message):
    """
    Универсальная функция для обработки действий с базой данных.

    :param self: Контекст класса
    :param connection: Соединение с базой данных
    :param input_fields: Словарь с объектами ввода, например:
                         {'client_id': self.id_line, 'client_fio': self.fio_line}
    :param sql_query: SQL-запрос для выполнения
    :param success_message: Сообщение об успешной операции
    :param error_message: Сообщение при ошибке
    """
    # Извлекаем значения из input_fields
    data = {key: field.text() for key, field in input_fields.items()}

    # Проверяем заполнение всех полей
    if not all(data.values()):
        QMessageBox.critical(self, "Ошибка", "Заполните все поля")
        return

    try:
        # Выполнение SQL-запроса
        cursor = connection.cursor()
        cursor.execute(sql_query, tuple(data.values()))
        connection.commit()
        cursor.close()

        # Успешное выполнение
        QMessageBox.information(self, "Успех", success_message)
        print(success_message)
    except(Exception, psycopg2.Error) as error:
        # Обработка ошибок
        QMessageBox.critical(self, "Ошибка", f"{error_message}: {error}")
        print(error_message, error)
        connection.rollback()
    finally:
        # Очистка полей ввода
        for field in input_fields.values():
            field.clear()

def show_everything(self, connection, table_widget, sql_query):
    """
       Универсальная функция для заполнения QTableWidget данными из базы данных.

       :param self: Родительский объект (например, self из класса)
       :param connection: Соединение с базой данных
       :param table_widget: QTableWidget, который нужно заполнить
       :param sql_query: SQL-запрос для получения данных
       """
    cursor = connection.cursor()
    try:
        # Выполняем запрос
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]

        # Настраиваем таблицу
        table_widget.setRowCount(len(rows))
        table_widget.setColumnCount(len(colnames))
        table_widget.setHorizontalHeaderLabels(colnames)
        table_widget.verticalHeader().setVisible(False)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Заполняем данные
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        cursor.close()
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при выводе данных: {e}")
        cursor.close()
        connection.rollback()