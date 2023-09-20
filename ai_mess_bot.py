import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from conf import bot_token, session
from handlers import control_handlers

dp = Dispatcher()


async def main() -> None:
    dp.include_router(control_handlers.router)
    bot = Bot(token=bot_token, session=session, parse_mode='HTML')
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
