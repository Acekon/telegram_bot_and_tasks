import os
from dotenv import load_dotenv

load_dotenv()
session = None
start_times = ['08:00', '12:00']
bot_token = os.getenv('TG_TOKEN')


def db_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, 'messages.db')
