import sqlite3
import json
import httpx
import os
import sys
import time
import signal

from config import (F_B_RACKS_COUNT,
                    F_B_SERVERS_COUNT,
                    F_B_PROTOCOL,
                    F_B_IP,
                    F_B_PORT,
                    F_B_PATH,
                    DEBUG,
                    TIMER)

DB_PATH = '../database/my_database.db'

URL = f"{F_B_PROTOCOL}://{F_B_IP}:{F_B_PORT}/{F_B_PATH}"
if DEBUG:
    URL = f'http://localhost:8080/freon/25_2'
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

def open_file(name_file):
    try:
        with open(name_file, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Файл не найден.")
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def create_id(tub: int, node: int):
    return int(tub*100+node)

def get_data_from_api(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")
        return None

def parse_response_data_FB (fa: dict):
    data_dict = {}
    ips = []
    error_ips = []
    for i_node in fb["rows"]:
        if i_node.get("name") is not ips:
            ips.append(i_node.get("name"))
            i_node_stat = i_node.get("stat")
            if i_node_stat != {}:
                i_node_coords = create_id(i_node_stat.get("coord").get("x"),
                                          i_node_stat.get("coord").get("y"))
                i_data = {
                    "name": i_node.get("name"),
                    "taskId": i_node.get("taskId"),
                    "state": i_node.get("state"),
                }
                number_unit = 1
                state_if_node = False
                if i_node.get("state") != "started":
                    state_if_node = True
                for i_unit in i_node_stat.get("units"):
                    i_unit_state = i_unit.get("state")
                    if state_if_node:
                        i_unit_state = i_node.get("state")
                    i_data[f"unit_{number_unit}"] = {
                        "unit.state": i_unit_state,
                        "unit.P": i_unit.get("P"),
                        "unit.T": i_unit.get("T"),
                        "unit.U": i_unit.get("U"),
                        "unit.I": i_unit.get("I")
                    }
                    number_unit += 1
                data_dict[i_node_coords] = i_data
        else:
            error_ips.append(i_node.get("name"))
        if len(error_ips) > 0:
            print("Ошибка в получении JSON")
    return data_dict

def update_data(data_dict):
    cursor = conn.cursor()
    data_to_update = [(json.dumps(value), key) for key, value in data_dict.items()]
    cursor.executemany("UPDATE fb SET data = ? WHERE id = ?;", data_to_update)
    print(f"Обновлено {cursor.rowcount} записей.")
    conn.commit()
    cursor.close()

try:
    while True:
        data_dict = {}
        id_count = 0
        start_time = time.time()
        fb = get_data_from_api(URL)
        get_time = time.time()
        if fb is not None:
            print("Есть связь")
            data_dict = parse_response_data_FB(fb)
            id_count = len(data_dict)
        else:
            print("СВЯЗИ НЕТ!")
        parser_time = time.time()
        for i in range(1, int(F_B_RACKS_COUNT) + 1):
            for j in range(1, int(F_B_SERVERS_COUNT) + 1):
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
              + "Добавление id:             " + str(add_time - parser_time) + "\n"
              + "Обновление БД:             " + str(update_time - add_time))
        # print(data_dict)
        time.sleep(int(TIMER))

except Exception as e:
    print(f"Ошибка: {e}")
