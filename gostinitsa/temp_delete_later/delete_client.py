import psycopg2
import csv
import os

try:
    connection = psycopg2.connect(
        database='Gostinitsa',
        user='postgres',
        password='Werere3601308wer',
        host='localhost',
        port='5432'
    )
    sql_query = 'DELETE FROM clienti;'
    cursor = connection.cursor()
    cursor.execute(sql_query)
    print("Удаление прошло успешно!")


except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL", error)