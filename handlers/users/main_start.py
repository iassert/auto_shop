# - *- coding: utf- 8 - *-
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import admins
from filters import IsPrivate
from keyboards.default import check_user_out_func
from loader import dp
from utils.db_api.sqlite import *
from utils.other_func import clear_firstname


# Обработка кнопки "На главную" и команды "/start"
@dp.message_handler(IsPrivate(), text="⬅ На главную", state="*")
@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = await get_settingsx()
    if get_settings[2] == "True" or str(message.from_user.id) in admins:
        first_name = clear_firstname(message.from_user.first_name)
        if message.from_user.username is None:
            get_status_user = await get_userx(user_id=message.from_user.id)
            if get_status_user is None:
                await add_userx(message.from_user.id, message.from_user.username, first_name,
                                0, 0, datetime.datetime.today().replace(microsecond=0))
            else:
                if get_status_user[3] != first_name:
                    await update_userx(user_id=message.from_user.id, user_name=first_name)
        else:
            get_status_user = await get_userx(user_login=message.from_user.username.lower())
            if get_status_user is None:
                await add_userx(message.from_user.id, message.from_user.username.lower(), first_name,
                                0, 0, datetime.datetime.today().replace(microsecond=0))
            else:
                if get_status_user[1] != message.from_user.id:
                    await delete_userx(user_id=get_status_user[1])
                    await add_userx(message.from_user.id, message.from_user.username.lower(), first_name,
                                    0, 0, datetime.datetime.today().replace(microsecond=0))
            get_status_user = await get_userx(user_id=message.from_user.id)
            if get_status_user is None:
                await add_userx(message.from_user.id, message.from_user.username.lower(), first_name,
                                0, 0, datetime.datetime.today().replace(microsecond=0))
            else:
                if get_status_user[3] != first_name:
                    await update_userx(user_id=message.from_user.id, user_name=first_name)
                if get_status_user[2] != message.from_user.username.lower():
                    await update_userx(user_id=message.from_user.id, user_login=message.from_user.username.lower())

        await message.answer("<b>🔸 Бот готов к использованию.</b>\n"
                             "🔸 Если не появились вспомогательные кнопки\n"
                             "▶ Введите /start",
                             reply_markup=check_user_out_func(message.from_user.id))
    else:
        await message.answer("<b>🔴 Бот находится на технических работах.</b>")
