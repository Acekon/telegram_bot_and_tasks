import time

from aiogram import Router

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InputFile, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.filters.command import Command

from handlers.db import search_mess, get_message_id, add_message
from handlers.img import get_collage, download_img
from conf import bot_token

router = Router()


class FormSearchText(StatesGroup):
    mess_search_text = State()


class FormGetId(StatesGroup):
    mess_id = State()


class FormAddMess(StatesGroup):
    text_message = State()


class FormGetIdImg(StatesGroup):
    mess_id = State()


@router.message(Command(commands=['search']))
async def command_get_search(message: Message, state: FSMContext):
    await state.set_state(FormSearchText.mess_search_text)
    await message.answer(f"Enter string for search")


@router.message(FormSearchText.mess_search_text)
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
    await state.set_state(FormGetId.mess_id)
    await message.answer(f"Enter ID message")


@router.message(FormGetId.mess_id)
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


@router.message(Command(commands=['newmessage']))
async def command_add_message(message: Message, state: FSMContext):
    await state.set_state(FormAddMess.text_message)
    await message.answer(f"Enter new message from save")


@router.message(FormAddMess.text_message)
async def process_mess_add(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    message_text = add_message(message.text)
    return await message.answer(message_text)


@router.message(Command(commands=['uploadimg']))
async def command_add_message(message: Message, state: FSMContext):
    await state.set_state(FormGetIdImg.mess_id)
    await message.answer(f"Upload file and Enter ID message:")


@router.message(FormGetIdImg.mess_id)
async def process_mess_add_img(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    if message.caption and message.caption.isdigit():
        file_id = message.photo[-1].file_id
        result = download_img(bot_token=bot_token, file_id=file_id, mess_id=message.caption)
        return await message.answer(result)
    else:
        return await message.answer('You not enter ID message')
