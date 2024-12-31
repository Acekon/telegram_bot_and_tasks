import logging
import os


def setup_logger():
    loggers = logging.getLogger('bot_logger')

    if not loggers.handlers:
        loggers.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'bot.log')
        access_log_handler = logging.FileHandler(filename=log_file_path, encoding='utf-8')
        access_log_handler.setLevel(logging.DEBUG)
        access_log_handler.setFormatter(formatter)
        loggers.addHandler(access_log_handler)

    return loggers


logger = setup_logger()
