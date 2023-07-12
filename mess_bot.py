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


if __name__ == '__main__':
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
