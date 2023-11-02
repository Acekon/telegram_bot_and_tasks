import os
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv

load_dotenv()

session = AiohttpSession(proxy="http://proxy2:3128/")

start_times = ['08:00', '12:00']
bot_token = f'{os.environ.get("bot_token")}'


def db_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, 'messages.db')
