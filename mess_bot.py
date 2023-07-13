import random
import string

import requests
from telebot.types import CallbackQuery, Message
import sqlite3
from conf import bot, admin_id, db_path, send_chat_id


@bot.message_handler(commands=['addmess'])
def command_add_mess(message: Message):
    if not message.chat.id == admin_id:
        return bot.send_message(message.chat.id, text=f'{message.chat.first_name} you do not have permission')
    bot.send_message(message.chat.id, "Enter text for save:")
    bot.register_next_step_handler(message, save_mess)


def save_mess(message: Message):
    text_mess = message.text
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute(f"INSERT INTO messages (text_message) VALUES ('{text_mess}')")
        conn.commit()
        c.execute('SELECT ids FROM messages ORDER BY ids DESC LIMIT 1')
        lats_sent = c.fetchone()
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, f"Saved! last ID= {lats_sent[0]}")
    except sqlite3.OperationalError as err:
        bot.send_message(admin_id, f"Not Save! Error: {err}")


@bot.message_handler(commands=['addimg'])
def command_add_img(message: Message):
    if not message.chat.id == admin_id:
        return bot.send_message(message.chat.id, text=f'{message.chat.first_name} you do not have permission')
    bot.send_message(admin_id, "Enter ID message this photo:")
    bot.register_next_step_handler(message, set_name_img)


def set_name_img(message: Message):
    if message.text.isdigit():
        bot.send_message(admin_id, "Waiting for you to upload file")
        bot.register_next_step_handler(message, upload_img, message.text)
    else:
        bot.send_message(admin_id, "ERROR: Name not int, need id (example: id)")
        command_add_img(message)


def upload_img(message: Message, name_img):
    response_img = requests.get(bot.get_file_url(message.json['photo'][2]['file_id']))
    if response_img.status_code != 200:
        return bot.send_message(admin_id, f"File not upload in server Http code: {response_img.status_code}")
    try:
        random_prefix_file = ''.join(random.choice(string.ascii_letters) for i in range(4))
        with open(f"img/{name_img}_{random_prefix_file}.png", 'wb') as f:
            f.write(response_img.content)
        return bot.send_message(admin_id, f"File {name_img}_{random_prefix_file}.png is uploads")
    except PermissionError as f:
        return bot.send_message(admin_id, f"File not upload in server: {f}")


@bot.message_handler(commands=['status'])
def command_check_status(message):
    sending_stats = check_last_sent_status()
    text_sending_stats = f'All messages = {sending_stats[0]}\nSend = {sending_stats[1]}\nNot Send = {sending_stats[2]}'
    bot.send_message(admin_id, f"{text_sending_stats}")


def check_last_sent_status():
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    c.execute(f'SELECT COUNT(ids) as total,'
              f'COUNT(last_send) as not_send, '
              f'COUNT(ids) - COUNT(last_send) as send '
              f'FROM messages;')
    lats_sent = c.fetchone()
    conn.commit()
    conn.close()
    return lats_sent


if __name__ == '__main__':
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
