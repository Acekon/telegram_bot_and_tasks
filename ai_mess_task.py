import datetime
import logging
import os
import random
import re
import sqlite3
import sys
import time

import requests
import schedule
import fnmatch
from conf import bot_token, db_path, start_times
from handlers.db import get_sendto, mess_reset, get_admins_list


def send_photo(file_path, caption, send_to):
    with open(file_path, 'rb') as img_file:
        img = {'photo': ('_', img_file, 'image/jpeg')}
        url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={send_to}&caption={caption}'
        response = requests.post(url, files=img)
        return response.text


def send_text(message_text, send_to):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    response = requests.post(url, json={'chat_id': send_to, 'parse_mode': 'html', 'text': message_text})
    return response.text


def send_random_message():
    channel_id = get_sendto()[0]
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE last_send is NULL AND enable is True')
    messages_db = c.fetchall()
    if len(messages_db) < 1:  # min count not send in db
        admins = get_admins_list()
        mess_text = mess_reset()
        for admin in admins:
            send_text(mess_text, admin[0])
    c.execute('SELECT ids, text_message, last_send  FROM messages WHERE last_send is NULL AND enable is True')
    messages_db = c.fetchall()
    message_db = messages_db[random.randint(0, len(messages_db) - 1)]
    message_id, text, last_sent = message_db
    img_mess = open_random_image(message_id)
    if img_mess:
        send_photo(file_path=os.path.join(os.getcwd(), img_mess), caption=text, send_to=channel_id)
    else:
        send_text(text, send_to=channel_id)
    c.execute('UPDATE messages SET last_send=? WHERE ids=?',
              (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), message_id))
    conn.commit()
    conn.close()


def get_send_last_img(message_id):
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    c.execute(f'SELECT last_img FROM messages WHERE ids={message_id}')
    messages_db = c.fetchone()
    return messages_db[0]


def save_last_img(message_id, file_name):
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    c.execute(f"UPDATE messages SET last_img='{file_name}' WHERE ids={message_id}")
    conn.commit()
    conn.close()


def open_random_image(message_id):
    img_files = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, 'img\\')
    pattern = f'{message_id}_*'
    for path, dirs, files in os.walk(source_dir):
        matched_strings = fnmatch.filter(files, pattern)
        for filename in matched_strings:
            fullpath = os.path.join(path, filename)
            img_files.append(fullpath)
        else:
            break
    if len(img_files) != 0:
        tmp_random_image = []
        for _ in range(10):
            tmp_random_image.append(random.randrange(0, len(img_files)))
        img = img_files[tmp_random_image[random.randrange(0, 8)]]
        return img
    else:
        return False


def main_run():
    print(f'Task will sending : {start_times}')
    for times in start_times:
        schedule.every().day.at(times).do(send_random_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    main_run()
