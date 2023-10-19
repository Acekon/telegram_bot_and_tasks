import functools
import logging
from aiogram.types import Message, CallbackQuery

from handlers.db import get_admins_list

logger = logging.getLogger('bot_logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s')
access_log_handler = logging.FileHandler(filename='logs/access.log', encoding='utf-8')
access_log_handler.setLevel(logging.DEBUG)
access_log_handler.setFormatter(formatter)
logger.addHandler(access_log_handler)
error_log_handler = logging.FileHandler(filename='logs/error.log', encoding='utf-8')
error_log_handler.setLevel(logging.WARNING)
error_log_handler.setFormatter(formatter)
logger.addHandler(error_log_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def auth_admin(func):
    @functools.wraps(func)
    async def wrapper(message=None, callback_query=None):
        admins_id = get_admins_list()
        if message:
            user_id = message.from_user.id
            user_command = message.text
            user_first_name = message.from_user.first_name
            user_last_name = message.from_user.last_name
        elif callback_query:
            user_id = callback_query.from_user.id
            user_command = callback_query.message.text
            user_first_name = callback_query.from_user.first_name
            user_last_name = callback_query.from_user.last_name
        else:
            return logger.debug(f'message:{message};callback_query:{callback_query}')
        logger.debug(f'user:{user_id};command:{user_command}')
        if user_id not in admins_id:
            logger.error(f'NOT PERMISSION: '
                         f'{user_id};{user_first_name};{user_last_name};{user_command}')
            return await message.answer(text=f'{user_first_name} you do not have permission')
        return await func(message)
    return wrapper

