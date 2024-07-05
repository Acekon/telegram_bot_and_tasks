import functools
import aiogram.types
from handlers.db import get_admins_list
from handlers.logger_setup import logger


def auth_admin(func):
    @functools.wraps(func)
    async def wrapper(message=None, *args, **kwargs):
        admins_id = get_admins_list()
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_last_name = message.from_user.last_name
        if isinstance(message, aiogram.types.callback_query.CallbackQuery):
            user_command = message.data
        elif isinstance(message, aiogram.types.message.Message):
            if message.caption:
                user_command = f'img_upload_id:{message.caption}'
            else:
                user_command = message.text
        else:
            user_command = f'Not support message type loging: {type(message)}'
        logger.debug(f'user:{user_id};command:{user_command}')
        if user_id not in [admin[0] for admin in admins_id]:
            logger.error(f'NOT PERMISSION: '
                         f'{user_id};{user_first_name};{user_last_name};{user_command}')
            return await message.answer(text=f'{user_first_name} you do not have permission')
        return await func(message, *args, **kwargs)

    return wrapper
