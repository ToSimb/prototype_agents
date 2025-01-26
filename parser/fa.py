import json


def open_file(name_file:str):
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

def create_id(x:int, y:int):
    return int(x*100+y)

try:
    platz, uzel = 16, 38
    data_dict = {}
    ips = []
    error_ips = []

    fa = open_file("json/22.json")
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
                    "units.P": i_stat.get("units")[0].get("P"),
                    "units.T": i_stat.get("units")[0].get("T"),
                    "units.U": i_stat.get("units")[0].get("U"),
                    "units.I": i_stat.get("units")[0].get("I"),
                }
                data_dict[i_coords] = i_data

        else:
            error_ips.append(i.get("name"))

    sorted_keys = sorted(data_dict.keys())
    for i in sorted_keys:
        print(i, data_dict[i])

    print(len(ips))
    print(len(error_ips))

except:
    print("Ошибка")
