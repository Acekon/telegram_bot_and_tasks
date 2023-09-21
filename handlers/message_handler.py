import time

from aiogram import types, Router, F
from aiogram.fsm import state

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery, BufferedInputFile, InputFile, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.filters.command import Command, CommandStart

from handlers.db import *
from handlers.img import get_collage

router = Router()


class Form_search_text(StatesGroup):
    mess_search_text = State()


class Form_get_id(StatesGroup):
    mess_id = State()


@router.message(Command(commands=['search']))
async def command_get_search(message: Message, state: FSMContext):
    await state.set_state(Form_search_text.mess_search_text)
    await message.answer(f"Enter string for search")


@router.message(Form_search_text.mess_search_text)
async def process_mess_search(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    messages = search_mess(message.text)
    if len(messages) <= 10:
        for mess in messages:
            await message.answer(f"ID = {mess[0]}\n{mess[1]}")
            time.sleep(0.2)
    else:
        await message.answer(f"Find {len(messages)}, please specify your request")


@router.message(Command(commands=['get']))
async def command_get_id(message: Message, state: FSMContext):
    await state.set_state(Form_get_id.mess_id)
    await message.answer(f"Enter ID message")


@router.message(Form_get_id.mess_id)
async def process_mess_get(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    message_text = get_message_id(message.text)
    if not message_text:
        return await message.answer(f"Not found")
    path_collage = get_collage(message.text)
    if path_collage:
        await message.answer_photo(FSInputFile(path_collage), caption=message_text[1])
    else:
        await message.answer(message_text[1])
