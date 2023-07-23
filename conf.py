import telebot
import os

bot_token  = f'{os.environ.get("tg_token")}'
admin_id = f'{os.environ.get("tg_admin_id")}'
send_chat_id = f'{os.environ.get("tg_id_channel")}'


start_times = ['08:00','12:00']
bot = telebot.TeleBot(bot_token)

def db_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, 'messages.db')
