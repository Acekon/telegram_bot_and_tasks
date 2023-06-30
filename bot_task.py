from telebot import types
import schedule
import random
import time
import datetime
import sqlite3
import os
from conf import start_times, db_path, send_chat_id, bot, admin_id


def send_message(send_chat_id):
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
    #debug_text = f"{message_id}, {text}, {last_sent},{(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"
    bot.send_message(chat_id=send_chat_id, text=f'{text}')
    c.execute('UPDATE messages SET last_send=? WHERE ids=?', (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), message_id))
    conn.commit()
    conn.close()




def run():
    print(f'Task will sending : {start_times}')
    for times in start_times:
        schedule.every().day.at(times).do(send_message,send_chat_id=f'{send_chat_id}')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
