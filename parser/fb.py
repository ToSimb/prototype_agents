import json

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

try:
    data_dict = {}
    ips = []
    error_ips = []

    fb = open_file("json/25-2.json")
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

    sorted_keys = sorted(data_dict.keys())
    for i_node in sorted_keys:
        print(i_node, data_dict[i_node])

    print(len(ips))
    print(len(error_ips))


except:
    print("Ошибка")
