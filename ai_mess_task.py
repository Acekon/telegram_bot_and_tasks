import asyncio
import logging
import sys
import time

import aiohttp
from aiogram import Bot
from conf import bot_token
from apscheduler.schedulers.asyncio import AsyncIOScheduler

start_times = ['08:00', '21:21']


async def sched():
    async with aiohttp.ClientSession() as client:
        bot = Bot(token=bot_token, parse_mode='HTML')
        CHANNEL_ID = '-1001431404849'
        message_text = f'message_text {time.time()}'
        await bot.send_message(chat_id=CHANNEL_ID, text=message_text)
        await client.close()




if __name__ == '__main__':
    m = 55
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sched, 'cron', hour=23, minute=m)
    scheduler.add_job(sched, 'cron', hour=23, minute=m + 1)
    scheduler.start()
    scheduler.run_until_stopped()