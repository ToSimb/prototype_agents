import sqlite3
import os
import json
import sys

from config import (F_A_True,
                    SERVERS_COUNT,
                    BOARDS_COUNT,
                    F_B_True)

def create_id(x:int, y:int):
    return int(x*100+y)

if F_A_True == F_B_True:
    print("В настройках не указан кокой именно изделие мониториться")
    sys.exit()  # Завершает выполнение программы

db_name = 'my_database.db'

if os.path.exists(db_name):
    os.remove(db_name)
    print(f"База данных {db_name} была удалена.")

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# ___________ FA ______________
if F_A_True:
    cursor.execute('''
    CREATE TABLE fa (
        id INTEGER PRIMARY KEY,
        data TEXT NOT NULL
    );
    ''')
    print("Создана новая таблица 'fa'.")

    # формирование индексов
    data_dict = {}
    for i in range(1, int(SERVERS_COUNT) + 1):
        for j in range(1, int(BOARDS_COUNT) + 1):
            key = create_id(i, j)
            if key not in data_dict:
                data_dict[key] = {}

    # Подготавливаем данные для вставки
    data_to_insert = [(int(key), json.dumps(value)) for key, value in data_dict.items()]

    cursor.executemany("INSERT INTO fa (id, data) VALUES (?, ?);", data_to_insert)
    print("Данные вставлены в таблицу 'fa'.")
    conn.commit()
conn.close()