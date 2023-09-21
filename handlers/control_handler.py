from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.markdown import hbold

from conf import admin_id
from aiogram.filters.command import Command, CommandStart

from handlers.db import check_last_sent_status, mess_reset

router = Router()


@router.message(Command(commands=['status']))
async def command_check_status(message):
    sending_stats = check_last_sent_status()
    text_sending_stats = (f'All messages = {sending_stats[0]}\n'
                          f'Available Send = {sending_stats[2]}\n'
                          f'Sented = {sending_stats[1]}')
    kb = [
        [types.InlineKeyboardButton(text="Reset sending message", callback_data=f'reset')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return await message.answer(f"{text_sending_stats}", reply_markup=keyboard)


@router.callback_query(F.data == 'reset')
async def command_mess_reset(message: CallbackQuery):
    return await message.answer(f"{mess_reset()}")


@router.message(CommandStart())
async def command_start_handler(message: Message) -> Message:
    if not message.chat.id in admin_id:
        return await message.answer(f"Hello, {hbold(message.from_user.full_name)} you do not have permission!")
    return await message.answer(f"Hello, {hbold(message.from_user.full_name)}")