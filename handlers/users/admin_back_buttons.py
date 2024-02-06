# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsPrivate, IsAdmin
from keyboards.default import payment_default, get_settings_func, get_functions_func, check_user_out_func, items_default
from loader import dp


# Обработка кнопки "К платёжным системам"
@dp.callback_query_handler(text="🔑 К платёжным системам ↩", state="*")
async def back_to_payments(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    await state.finish()
    await message.edit_text("🔑 Настройка платежных системы.", reply_markup= await payment_default())


# Обработка кнопки "К настройкам"
@dp.callback_query_handler(text="⚙ К настройкам ↩", state="*")
async def back_to_settings(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    await state.finish()
    await message.edit_text("⚙ Основные настройки бота.", reply_markup= await get_settings_func())


# Обработка кнопки "К общим функциям"
@dp.callback_query_handler(text="🔆 К общим функциям", state="*")
async def back_to_functions(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    await state.finish()
    await message.edit_text("🔆 Выберите нужную функцию.", reply_markup=get_functions_func(message.from_user.id))


# Обработка кнопки "К управлению товарами"
@dp.callback_query_handler(text="🎁 К управлению товарами ↩", state="*")
async def back_to_edit_items(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    await state.finish()
    await message.edit_text("🎁 Редактирование товаров, разделов и категорий 📜",
                         reply_markup=items_default)


