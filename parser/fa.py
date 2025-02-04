import sqlite3
import json
import httpx
import os
import sys
import time
import signal

from config import (F_A_True,
                    SERVERS_COUNT,
                    BOARDS_COUNT,
                    F_A_PROTOCOL,
                    F_A_IP,
                    F_A_PORT,
                    F_A_PATH,
                    DEBUG,
                    TIMER)

DB_PATH = '../database/my_database.db'

URL = f"{F_A_PROTOCOL}://{F_A_IP}:{F_A_PORT}/{F_A_PATH}"
if DEBUG:
    URL = f'http://localhost:8080/freon/22'
print(URL)

if not os.path.exists(DB_PATH):
    print(f"Ошибка: база данных {DB_PATH} не найдена.")
    sys.exit(1)
conn = sqlite3.connect(DB_PATH)
print("успешное соединение с БД")

def signal_handler(sig, frame):
    print("Принят сигнал завершения работы. Закрытие соединения...")
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def create_id(x:int, y:int):
    return int(x*100+y)

def parse_response_data_FA (fa: dict):
    data_dict = {}
    ips = []
    error_ips = []
    for i in fa["rows"]:
        if i.get("name") is not ips:
            ips.append(i.get("name"))
            i_stat = i.get("stat")
            if i_stat != {}:
                i_coords = create_id(i_stat.get("coord").get("x"),
                                     i_stat.get("coord").get("y"))
                i_data = {
                    "name": i.get("name"),
                    "taskId": i.get("taskId"),
                    "state": i.get("state"),
                    "unit.P": i_stat.get("units")[0].get("P"),
                    "unit.T": i_stat.get("units")[0].get("T"),
                    "unit.U": i_stat.get("units")[0].get("U"),
                    "unit.I": i_stat.get("units")[0].get("I"),
                }
                data_dict[i_coords] = i_data

        else:
            error_ips.append(i.get("name"))
        if len(error_ips) > 0:
            print("Ошибка в получении JSON")
    return data_dict

def get_data_from_api(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")
        return None

def update_data(data_dict):
    cursor = conn.cursor()
    data_to_update = [(json.dumps(value), key) for key, value in data_dict.items()]
    cursor.executemany("UPDATE fa SET data = ? WHERE id = ?;", data_to_update)
    print(f"Обновлено {cursor.rowcount} записей.")
    conn.commit()
    cursor.close()

try:
    while True:
        data_dict = {}
        id_count = 0
        start_time = time.time()
        fa = get_data_from_api(URL)
        get_time = time.time()
        if fa is not None:
            print("Есть связь")
            data_dict = parse_response_data_FA(fa)
            id_count = len(data_dict)
        parser_time = time.time()
        for i in range(1, int(SERVERS_COUNT) + 1):
            for j in range(1, int(BOARDS_COUNT) + 1):
                key = create_id(i, j)
                if key not in data_dict:
                    data_dict[key] = {}
        add_time = time.time()
        update_data(data_dict)
        update_time = time.time()
        print("______________" + "\n"
              + "Получение данных:          " + str(get_time - start_time) + "\n"
              + "Форматирование данных:     " + str(parser_time - get_time) + "\n"
              + "Количество полученных id:  " + str(id_count) + "/" + str(len(data_dict)) + "\n"
              + "Добавление id:             " + str(add_time-parser_time) + "\n"
              + "Обновление БД:             " + str(update_time-add_time))
        # print(data_dict)
        time.sleep(int(TIMER))



except Exception as e:
    print(f"Ошибка: {e}")
