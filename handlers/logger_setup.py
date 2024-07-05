import logging


def setup_logger():
    logger = logging.getLogger('bot_logger')

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

        access_log_handler = logging.FileHandler(filename='logs/bot.log', encoding='utf-8')
        access_log_handler.setLevel(logging.DEBUG)
        access_log_handler.setFormatter(formatter)
        logger.addHandler(access_log_handler)

    return logger


logger = setup_logger()
