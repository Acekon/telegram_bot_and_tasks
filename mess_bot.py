import fnmatch
import os
import random
import string
import time

import requests
from PIL import Image
from telebot import types
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
        random_prefix_file = ''.join(random.choice(string.ascii_letters) for i in range(6))
        with open(f"img/{name_img}_{random_prefix_file}.png", 'wb') as f:
            f.write(response_img.content)
        return bot.send_message(admin_id, f"File {name_img}_{random_prefix_file}.png is uploads")
    except PermissionError as f:
        return bot.send_message(admin_id, f"File not upload in server: {f}")


@bot.message_handler(commands=['status'])
def command_check_status(message):
    if not message.chat.id == admin_id:
        return bot.send_message(message.chat.id, text=f'{message.chat.first_name} you do not have permission')
    sending_stats = check_last_sent_status()
    text_sending_stats = (f'All messages = {sending_stats[0]}\n'
                          f'Available Send = {sending_stats[2]}\n'
                          f'Sented = {sending_stats[1]}')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton('Reset sending message', callback_data=f'reset'), ]
    keyboard.add(*buttons)
    bot.send_message(admin_id, f"{text_sending_stats}", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('reset'))
def command_mess_reset(message: CallbackQuery):
    if not message.from_user.id == admin_id:
        return bot.send_message(message.from_user.id, text=f'{message.from_user.first_name} you do not have permission')
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute('UPDATE messages SET last_send = NULL;')
        conn.commit()
        bot.send_message(chat_id=admin_id, text=f'History sending messages is reset, new iteration started.')
        conn.close()
    except sqlite3.OperationalError as err:
        bot.send_message(admin_id, f"Not reset! Error: {err}")


@bot.message_handler(commands=['getmess'])
def command_get_mess(message):
    if not message.chat.id == admin_id:
        return bot.send_message(message.chat.id, text=f'{message.chat.first_name} you do not have permission')
    bot.send_message(admin_id, "Enter ID message")
    bot.register_next_step_handler(message, get_message_id)


def get_message_id(message: Message):
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute(f'SELECT ids, text_message FROM messages WHERE ids="{message.text}"')
        mess = c.fetchone()
        conn.commit()
        conn.close()
        if mess:
            matching_files = []
            files_name = []
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton('💥 Remove message and img', callback_data=f'mess|remove:{message.text}'),
                types.InlineKeyboardButton('💥 Remove IMG', callback_data=f'mess|remove|img:{message.text}'),
                types.InlineKeyboardButton('🟢 Replace', callback_data=f'mess|replace:{message.text}'),
                types.InlineKeyboardButton('🟡 Cancel', callback_data=f'mess|cancel')]
            keyboard.add(*buttons)
            for file_name in os.listdir('img/'):
                if fnmatch.fnmatch(file_name, f'{message.text}_*.png'):
                    matching_files.append(os.path.abspath('img//' + file_name))
                    files_name.append(file_name)
            if matching_files:
                create_image_collage(matching_files)
                bot.send_photo(chat_id=admin_id, photo=open('collage.png', 'rb'),
                               caption=f'{mess[1]}\n\nFile list:\n{files_name}', reply_markup=keyboard)
                if os.path.isfile('collage.png'):
                    os.remove('collage.png')
            else:
                bot.send_message(admin_id, f"{mess[1]}!", reply_markup=keyboard)
        else:
            bot.send_message(admin_id, f"ID is not found")
    except sqlite3.OperationalError as err:
        bot.send_message(admin_id, f"Error: {err}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('mess|remove'))
def command_mess_remove(message: CallbackQuery):
    if not message.from_user.id == admin_id:
        return bot.send_message(message.from_user.id, text=f'{message.from_user.first_name} you do not have permission')
    if message.message.content_type == 'photo':
        remove_mess(message.data.split(':')[1])
    elif message.message.content_type == 'text':
        remove_mess(message.data.split(':')[1])
    else:
        bot.send_message(admin_id, f"Error: content_type not supported ({message.message.content_type})")


def remove_mess(id_mess):
    try:
        matching_files = []
        for file_name in os.listdir('img/'):
            if fnmatch.fnmatch(file_name, f'{id_mess}_*.png'):
                matching_files.append(os.path.abspath('img//' + file_name))
        for name_file in matching_files:
            if os.path.isfile(name_file):
                os.remove(name_file)
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        count = c.execute(f'DELETE FROM messages WHERE ids = "{id_mess}"').rowcount
        conn.commit()
        conn.close()
        if count != 0:
            bot.send_message(admin_id, f"ID= {id_mess}. Removed from DB")
        else:
            bot.send_message(admin_id, f"ID= {id_mess}. Not found from DB")

    except sqlite3.OperationalError as err:
        bot.send_message(admin_id, f"Error: {err}")


def create_image_collage(image_paths, output_path='collage.png'):
    image_size = (200, 200)
    collage_size = (image_size[0] * len(image_paths), image_size[1])
    collage = Image.new('RGB', collage_size)
    for i, image_path in enumerate(image_paths):
        image = Image.open(image_path)
        image = image.resize(image_size)
        collage.paste(image, (i * image_size[0], 0))
    collage.save(output_path)


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


@bot.message_handler(commands=['search'])
def command_get_search(message):
    if not message.chat.id == admin_id:
        return bot.send_message(message.chat.id, text=f'{message.chat.first_name} you do not have permission')
    bot.send_message(admin_id, "Enter string for search")
    bot.register_next_step_handler(message, get_message_search)


def get_message_search(message: Message):
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute(f'SELECT ids, text_message FROM messages WHERE text_message like "%{message.text}%"')
        messages = c.fetchall()
        conn.commit()
        conn.close()
        if not messages:
            bot.send_message(admin_id, f"Not found")
        if len(messages) <= 10:
            for mess in messages:
                bot.send_message(admin_id, f"ID = {mess[0]}\n{mess[1]}")
                time.sleep(0.2)
        else:
            bot.send_message(admin_id, f"Find {len(messages)} please specify your request ")
    except sqlite3.OperationalError as err:
        bot.send_message(admin_id, f"Error: {err}")

if __name__ == '__main__':
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
