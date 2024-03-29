# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsPrivate, IsAdmin
from keyboards.default import get_settings_func, payment_default, get_functions_func, items_default, admins
from keyboards.inline import choice_way_input_payment_func, on_main
from loader import dp, bot
from utils.db_api.sqlite import *


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Платежные системы"
@dp.callback_query_handler(text="🔑 Платежные системы", state="*")
async def payments_systems(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...
    
    await state.finish()
    await message.answer("🔑 Настройка платежных системы.", reply_markup= await payment_default())
    await message.answer("🥝 Выберите способ пополнения 💵\n"
                         "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                         "🔸 <a href='https://vk.cc/bYjKGM'><b>По форме</b></a> - <code>Готовая форма оплаты QIWI</code>\n"
                         "🔸 <a href='https://vk.cc/bYjKEy'><b>По номеру</b></a> - <code>Перевод средств по номеру телефона</code>\n"
                         "🔸 <a href='https://vk.cc/bYjKJk'><b>По никнейму</b></a> - "
                         "<code>Перевод средств по никнейму (пользователям придётся вручную вводить комментарий)</code>",
                         reply_markup= await choice_way_input_payment_func())


# Обработка кнопки "Настройки бота"
@dp.callback_query_handler(text="⚙ Настройки", state="*")
async def settings_bot(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await state.finish()
    await message.answer("⚙ Основные настройки бота.", reply_markup= await get_settings_func())


# Обработка кнопки "Общие функции"
@dp.callback_query_handler(text="🔆 Общие функции", state="*")
async def general_functions(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await state.finish()
    await message.answer("🔆 Выберите нужную функцию.", reply_markup=get_functions_func(call.from_user.id))


# Обработка кнопки "Общие функции"
@dp.callback_query_handler(text="📰 Информация о боте", state="*")
async def general_functions(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await state.finish()
    about_bot = await get_about_bot()
    await message.answer(about_bot, reply_markup=on_main)


# Обработка кнопки "Управление товарами"
@dp.callback_query_handler(text="🎁 Управление товарами 🖍", state="*")
async def general_functions(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await state.finish()
    await message.answer(
        "🎁 Редактирование товаров, разделов и категорий 📜",
                         reply_markup=items_default
            )


# Получение БД
@dp.message_handler(IsPrivate(), IsAdmin(), commands="getbd", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    for admin in admins:
        with open("data/botBD.sqlite", "rb") as doc:
            await bot.send_document(admin,
                                    doc,
                                    caption=f"📦 <b>BACKUP</b>\n🕜 <code>{datetime.datetime.today().replace(microsecond=0)}</code>")


async def get_about_bot():
    show_profit_all, show_profit_day, show_refill, show_buy_day, show_money_in_bot, show = 0, 0, 0, 0, 0, 0
    get_settings = await get_settingsx()
    all_purchases = await get_all_purchasesx()
    all_users = await get_all_usersx()
    all_refill = await get_all_refillx()
    show_users = await get_all_usersx()
    show_categories = await get_all_categoriesx()
    show_positions = await get_all_positionsx()
    show_items = await get_all_itemsx()
    for purchase in all_purchases:
        show_profit_all += float(purchase[6])
        if float(get_settings[4]) - float(purchase[14]) < 86400:
            show_profit_day += float(purchase[6])
    for user in all_users:
        show_money_in_bot += float(user[4])
    for refill in all_refill:
        show_refill += float(refill[5])
        if float(get_settings[5]) - float(refill[9]) < 86400:
            show_buy_day += float(refill[5])
    message = "<b>📰 ВСЯ ИНФОРАМЦИЯ О БОТЕ</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Пользователи:</b> 🔶\n" \
              f"👤 Пользователей: <code>{len(show_users)}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Средства</b> 🔶\n" \
              f"📗 Продаж за 24 часа на: <code>{show_profit_day}$</code>\n" \
              f"💰 Продано товаров на: <code>{show_profit_all}$</code>\n" \
              f"📕 Пополнений за 24 часа: <code>{show_buy_day}$</code>\n" \
              f"💳 Средств в системе: <code>{show_money_in_bot}$</code>\n" \
              f"🥝 Пополнено: <code>{show_refill}$</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Прочее</b> 🔶\n" \
              f"🎁 Товаров: <code>{len(show_items)}</code>\n" \
              f"📁 Позиций: <code>{len(show_positions)}</code>\n" \
              f"📜 Категорий: <code>{len(show_categories)}</code>\n" \
              f"🛒 Продано товаров: <code>{len(all_purchases)}</code>\n"
    return message


# Получение списка всех товаров
@dp.message_handler(IsPrivate(), IsAdmin(), commands="getitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = await get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары</b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             "📍 <code>айди товара - данные товара</code>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            save_items.append(f"📍 <code>{item[1]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>")


# Получение списка всех позиций
@dp.message_handler(IsPrivate(), IsAdmin(), commands="getposition", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = await get_all_positionsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>📁 Все позиции</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            save_items.append(f"<code>{item[2]}</code>")
        if len_items >= 35:
            count_split = round(len_items / 35)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>📁 Позиции отсутствуют</b>")


# Получение подробного списка всех товаров
@dp.message_handler(IsPrivate(), IsAdmin(), commands="getinfoitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = await get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары и их позиции</b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            get_position = await get_positionx("*", position_id=item[3])
            save_items.append(f"<code>{get_position[2]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>")
