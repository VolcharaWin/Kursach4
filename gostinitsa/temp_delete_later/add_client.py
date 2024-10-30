import psycopg2
import csv
import os
# Путь к SQL файлу
sql_file_path = 'add_client.sql'

# Путь к файлу с данными
data_file_path = 'clienti.csv'

try:
    # Подключение к базе данных
    connection = psycopg2.connect(
        database="Gostinitsa",
        user="postgres",
        password="Werere3601308wer",
        host="localhost",
        port="5432"
    )
    if not os.path.exists(sql_file_path):
        print("add_client не найден!")
    else:
        print("add_client доступен для чтения!")
    # Открываем и читаем файл с SQL-запросом
    with open(sql_file_path, 'r') as sql_file:
        sql_query = sql_file.read()

    # Создаем курсор
    cursor = connection.cursor()

    # Открываем файл с данными и читаем строки
    if not os.path.exists(data_file_path):
        print("clienti не найден!")
    else:
        print("clienti доступен для чтения!")
    with open(data_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Удаляем пробелы в данных (например, в номере телефона)
            row = [item.strip() for item in row]
            # Выполняем запрос на вставку для каждой строки данных
            cursor.execute(sql_query, row)

    # Подтверждаем транзакцию
    connection.commit()

    # Закрываем курсор
    cursor.close()

except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

finally:
    if connection:
        # Закрытие подключения
        connection.close()
        print("Соединение с PostgreSQL закрыто")