from telebot import types
import schedule
import random
import time
import datetime
import sqlite3
import os
from conf import start_times, db_path, send_chat_id, bot, admin_id


def send_message(send_chat_id):
    print(f"Debug {(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} sending")
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE last_send is NULL')
    messages_db = c.fetchall()
    if len(messages_db) < 1:
        c.execute('UPDATE messages SET last_send = NULL;')
        conn.commit()
        bot.send_message(chat_id=admin_id, text=f'History sending messages is reset, new iteration started.')
    c.execute('SELECT * FROM messages WHERE last_send is NULL')
    messages_db = c.fetchall()
    message_db = messages_db[random.randint(0, len(messages_db) - 1)]
    message_id, text, last_sent = message_db
    img_mess = open_image(message_id)
    if img_mess:
        send_photo(text, img_mess=img_mess)
    else:
        send_text(text)
    c.execute('UPDATE messages SET last_send=? WHERE ids=?', (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), message_id))
    conn.commit()
    conn.close()


def send_text(text):
    bot.send_message(chat_id=send_chat_id, text=f'{text}')


def send_photo(text, img_mess):
    bot.send_photo(chat_id=send_chat_id, photo=open(img_mess, 'rb'), caption=f'{text}')


def open_image(message_id):
    source_dir = 'img/'
    img_files = []
    for path, dirs, files in os.walk(source_dir):
        for filename in files:
            fullpath = os.path.join(path, filename)
            if int(filename.split('_')[0]) == message_id:
                img_files.append(fullpath)
            else:
                if len(img_files) >= 1:
                    break
                continue
    if len(img_files) != 0:
        img = img_files[random.randrange(0, len(img_files))]
        return img
    else:
        return False


def run():
    print(f'Task will sending : {start_times}')
    for times in start_times:
        schedule.every().day.at(times).do(send_message,send_chat_id=f'{send_chat_id}')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
