import sqlite3

from conf import db_path


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


def mess_reset():
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute('UPDATE messages SET last_send = NULL;')
        conn.commit()
        conn.close()
        return f'History sending messages is reset, new iteration started.'
    except sqlite3.OperationalError as err:
        return f"Not reset! Error: {err}"
