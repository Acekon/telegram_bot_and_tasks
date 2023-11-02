import os

from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy="http://proxy2:3128/")
start_times = ['08:00', '12:00']
bot_token = '999904733:AAGaeFxiu7yXLxlP_tt9btRiM_ffWBpNFOo'
admin_id = f'{os.environ.get("tg_admin_id")}'
send_chat_id = f'{os.environ.get("tg_id_channel")}'


def db_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, 'messages.db')
