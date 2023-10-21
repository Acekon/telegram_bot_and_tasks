import asyncio
import logging
import os
import sys
import argparse
from aiogram import Bot, Dispatcher

from conf import bot_token, session, db_path
from handlers import control_handler, message_handler
from handlers.db import create_all_table, add_admin_list

dp = Dispatcher()


async def main() -> None:
    dp.include_router(control_handler.router)
    dp.include_router(message_handler.router)
    bot = Bot(token=bot_token, session=session, parse_mode='HTML')
    await dp.start_polling(bot)


def create_dirs():
    directory_path = os.path.dirname(os.path.realpath(__file__))
    folder_names = ["img", "logs"]
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    for folder_name in folder_names:
        folder_path = os.path.join(directory_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


def create_admin(admin):
    try:
        admin_id, description = admin.split(',')
        if not admin_id.isdigit():
            raise SystemExit(f'Err: {admin_id} not INT')
        result = add_admin_list(admin_id, description)
        if result:
            return f'Add: {admin_id}, {description}'
        else:
            raise SystemExit(f'Err: {admin_id}, {description}\n {result}')
    except ValueError:
        return 'Err: required\n<b>12345678,NameAdmin</b>'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bot Control')
    parser.add_argument('--run', action='store_true', help='Run the bot')
    parser.add_argument('--generate', action='store_true', help='Generate empty DB and directory')
    parser.add_argument('--createadmin', help='Create admin for bot need "AdminID,Name"')
    args = parser.parse_args()
    if args.run:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    elif args.generate:
        create_dirs()
        db_path()
        create_all_table()
    elif args.createadmin:
        create_admin(args.createadmin)
    else:
        raise SystemExit('Need usage --run')
