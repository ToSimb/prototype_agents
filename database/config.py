import os

from dotenv import load_dotenv


def str_to_bool(value):
    if value.lower() in ('true', '1', 't', 'y', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'f', 'n', 'no'):
        return False
    else:
        raise ValueError(f"Invalid truth value: {value}")

load_dotenv()

# настройка API F-A
F_A_True = os.environ.get('F_A_True')
F_A_SERVERS_COUNT = os.environ.get('F_A_SERVERS_COUNT')
F_A_BOARDS_COUNT = os.environ.get('F_A_BOARDS_COUNT')
F_A_PROTOCOL = os.environ.get('F_A_PROTOCOL')
F_A_IP = os.environ.get('F_A_IP')
F_A_PORT = os.environ.get('F_A_PORT')
F_A_PATH = os.environ.get('F_A_PATH')

# настройка API F-B
F_B_True = os.environ.get('F_B_True')
F_B_RACKS_COUNT = os.environ.get('F_B_RACKS_COUNT')
F_B_SERVERS_COUNT = os.environ.get('F_B_SERVERS_COUNT')
F_B_PROTOCOL = os.environ.get('F_B_PROTOCOL')
F_B_IP = os.environ.get('F_B_IP')
F_B_PORT = os.environ.get('F_B_PORT')
F_B_PATH = os.environ.get('F_B_PATH')

# общие
DEBUG = str_to_bool(os.environ.get("DEBUG", "false"))
TIMER = os.environ.get('TIMER')

