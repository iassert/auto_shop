# - *- coding: utf- 8 - *-
import os
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from data.config import admins
from filters import IsPrivate
from keyboards.default import check_user_out_func
from keyboards.inline.user_inline import on_main, menu
from keyboards.inline.user_profiles import get_user_profile
from loader import dp
from utils.db_api.sqlite import *
from utils.other_func import clear_firstname


# Обработка кнопки "На главную" и команды "/start"
@dp.message_handler(IsPrivate(), text="Меню", state="*")
@dp.message_handler(IsPrivate(), text_startswith="/start", state="*")
async def bot_start(message: types.Message, state: FSMContext):
    from .user_menu import position

    args = message.text.split(' ')
    if len(args) == 2: 
        data = args[1].split('_')
        
        if len(data) == 3:
            sPosition_id, sRemover, sCategory_id = data
            
            await add_update(
                message.from_user.id, 
                message.from_user.first_name, 
                message.from_user.username
            )

            return await position(
                message.from_user.id,
                sPosition_id,
                sRemover,
                sCategory_id,
                message
            )

    await _bot_start(
        message, 
        state, 
        message.from_user.id, 
        message.from_user.first_name, 
        message.from_user.username
    )

@dp.callback_query_handler(text="⬅ На главную", state="*")
async def call_bot_start(call: CallbackQuery, state: FSMContext):
    await _bot_start(
        call.message, 
        state, 
        call.from_user.id, 
        call.from_user.first_name, 
        call.from_user.username
    )

async def _bot_start(message: types.Message, state: FSMContext, from_user_id: int, first_name: str, username: str | None):
    await state.finish()
    get_settings = await get_settingsx()
    if get_settings[2] == "True" or str(from_user_id) in admins:
        await add_update(from_user_id, first_name, username)

        t = "<b>🔸 Бот готов к использованию.</b>\n"\
            "🔸 Если не появились вспомогательные кнопки\n"\
            "▶ Введите /start"
        
        markup=check_user_out_func(from_user_id)
        get_user = await get_user_profile(from_user_id)

        if message.from_user.is_bot:
            try:
                await message.delete()
            except:
                ...

        return await message.answer_photo(InputFile("./photo/main_menu.jpg"), get_user, reply_markup = markup)

    t = "<b>🔴 Бот находится на технических работах.</b>"
    if message.from_user.is_bot:
        return await message.edit_text(t, reply_markup = on_main)

    await message.answer(t, reply_markup = on_main)

async def add_update(from_user_id: int, first_name: str, username: str | None):
    first_name = clear_firstname(first_name)
    if username is None:
        get_status_user = await get_userx(user_id=from_user_id)
        if get_status_user is None:
            await add_userx(from_user_id, username, first_name,
                            0, 0, datetime.datetime.today().replace(microsecond=0))
        else:
            if get_status_user[3] != first_name:
                await update_userx(user_id=from_user_id, user_name=first_name)
    else:
        get_status_user = await get_userx(user_login=username.lower())
        if get_status_user is None:
            await add_userx(from_user_id, username.lower(), first_name,
                            0, 0, datetime.datetime.today().replace(microsecond=0))
        else:
            if get_status_user[1] != from_user_id:
                await delete_userx(user_id=get_status_user[1])
                await add_userx(from_user_id, username.lower(), first_name,
                                0, 0, datetime.datetime.today().replace(microsecond=0))
        get_status_user = await get_userx(user_id=from_user_id)
        if get_status_user is None:
            await add_userx(from_user_id, username.lower(), first_name,
                            0, 0, datetime.datetime.today().replace(microsecond=0))
        else:
            if get_status_user[3] != first_name:
                await update_userx(user_id=from_user_id, user_name=first_name)
            if get_status_user[2] != username.lower():
                await update_userx(user_id=from_user_id, user_login=username.lower())