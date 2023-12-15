import os
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv

load_dotenv()

session = None

start_times = ['10:21', '10:22', '10:23']
bot_token = f'{os.environ.get("bot_token")}'


def db_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, 'messages.db')
