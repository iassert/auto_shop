# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import admins
from filters import IsPrivate, IsAdmin
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.inline import *
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.state_users import *
from utils.other_func import clear_firstname

from .main_start import bot_start, call_bot_start

# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Купить"
@dp.callback_query_handler(text="💳 Купить", state="*")
async def show_search(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await state.finish()
    get_settings = await get_settingsx()
    get_user = await get_user_profile(call.from_user.id)
    if get_settings[2] == "True" or str(call.from_user.id) in admins:
        if get_user is not None:
            if get_settings[3] == "True" or str(call.from_user.id) in admins:
                get_categories = await get_all_categoriesx()
                if len(get_categories) >= 1:
                    get_kb = await buy_item_open_category_ap(0)
                    await message.answer("<b>🎁 Выберите нужный вам товар:</b>", reply_markup=get_kb)
                else:
                    await message.answer("<b>🎁 Товары в данное время отсутствуют.</b>", reply_markup=on_main)
            else:
                await message.answer("<b>🔴 Покупки в боте временно отключены.</b>", reply_markup=on_main)
        else:
            await message.answer("<b>❗ Ваш профиль не был найден.</b>\n▶ Введите /start", reply_markup=on_main)
    else:
        await message.answer("<b>🔴 Бот находится на технических работах.</b>", reply_markup=on_main)


# Обработка кнопки "Профиль"
@dp.callback_query_handler(text="📱 Профиль", state="*")
async def show_profile(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    await state.finish()
    get_settings = await get_settingsx()
    get_status_user = await get_user_profile(call.from_user.id)
    if get_settings[2] == "True" or str(call.from_user.id) in admins:
        if get_status_user is not None:
            await message.edit_text(get_status_user, reply_markup=open_profile_inl)
        else:
            await message.edit_text("<b>❗ Ваш профиль не был найден.</b>\n▶ Введите /start", reply_markup=on_main)
    else:
        await message.edit_text("<b>🔴 Бот находится на технических работах.</b>", reply_markup=on_main)


# Обработка кнопки "FAQ"
@dp.callback_query_handler(text="ℹ FAQ", state="*")
async def show_my_deals(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await state.finish()
    get_settings = await get_settingsx()
    get_status_user = await get_userx(user_id=call.from_user.id)
    if get_settings[2] == "True" or str(call.from_user.id) in admins:
        if get_status_user is not None:
            await message.answer(bot_description, reply_markup=on_main)
        else:
            await message.answer("<b>❗ Ваш профиль не был найден.</b>\n▶ Введите /start", reply_markup=on_main)
    else:
        await message.answer("<b>🔴 Бот находится на технических работах.</b>", reply_markup=on_main)


# Обработка кнопки "Поддержка"
@dp.callback_query_handler(text="💬 Поддержка", state="*")
async def show_contact(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    await state.finish()

    try:
        await message.delete()
    except:
        ...

    get_settings = await get_settingsx()
    get_status_user = await get_userx(user_id=call.from_user.id)
    
    if get_settings[2] == "True" or str(call.from_user.id) in admins:
        if get_status_user is not None:
            await message.answer("✍️<b>Опишите проблему\n▶ И\или прикрепите 📸 фото с описанием проблемы</b>", reply_markup=on_main)
            return await StorageUsers.write_support.set()
        return await message.answer("<b>❗ Ваш профиль не был найден.</b>\n▶ Введите /start", reply_markup=on_main)

    await message.answer("<b>🔴 Бот находится на технических работах.</b>", reply_markup=on_main)


@dp.message_handler(content_types=["text", "photo"], state=StorageUsers.write_support)
async def write_support(message: types.Message, state: FSMContext):
    text = f"<b>👤 Пользователь</b> "\
        f"(@{message.from_user.username}|<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"\
        f"|<code>{message.from_user.id}</code>) "
    
    for admin_id in admins:
        try:
            msg = ""
            if message.text:
                msg = message.text
            elif message.caption:
                msg = message.caption

            msg = f"💬 Обращение в тех поддержку\n\n{msg}\n\n{text}"

            if message.photo:
                await bot.send_photo(admin_id, message.photo[-1].file_id)
            await bot.send_message(admin_id, msg, reply_markup=reply_support(message.from_user.id))
        except BaseException as ex:
            logging.error(f"{ex.__class__.__name__}: {ex}")
    await message.answer("👍 Спасибо за обраную связь, сообщение отправленно")
    await bot_start(message, state)
    await state.finish()

@dp.callback_query_handler(text_startswith="reply_support")
async def reply_support_msg(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    async with state.proxy() as data:
        data["reply_support_id"] = int(call.data.split(':')[1])

    await message.answer(f"✍️ Введите сообщение")
    await StorageUsers.reply_support.set()


@dp.message_handler(content_types="text", state=StorageUsers.reply_support)
async def send_msg_(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        reply_support_id = data["reply_support_id"]

    await bot.send_message(reply_support_id, f"💬 Сообщение от тех поддержки\n\n{message.text}")
    await message.answer("✅Сообщение отправленно")

    await state.finish()

# Обработка колбэка "Мои покупки"
@dp.callback_query_handler(text="my_buy")
async def show_referral(call: CallbackQuery, state: FSMContext):
    last_purchases = await last_purchasesx(call.from_user.id)
    if len(last_purchases) >= 1:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        count_split = 0
        save_purchases = []
        for purchases in last_purchases:
            save_purchases.append(f"<b>📃 Чек:</b> <code>#{purchases[4]}</code>\n"
                                  f"▶ {purchases[9]} | {purchases[5]}шт | {purchases[6]}$\n"
                                  f"🕜 {purchases[13]}\n"
                                  f"<code>{purchases[10]}</code>")
        await bot.send_message(call.from_user.id,
                               "<b>🛒 Последние 10 покупок</b>\n"
                               "➖➖➖➖➖➖➖➖➖➖➖➖➖")
        save_purchases.reverse()
        len_purchases = len(save_purchases)
        if len_purchases > 4:
            count_split = round(len_purchases / 4)
            count_split = len_purchases // count_split
        if count_split > 1:
            get_message = split_messages(save_purchases, count_split)
            for msg in get_message:
                send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(msg)
                await bot.send_message(call.from_user.id, send_message)
        else:
            send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(save_purchases)
            await bot.send_message(call.from_user.id, send_message)

        await call_bot_start(call, state)
    else:
        await bot.answer_callback_query(call.id, "❗ У вас отсутствуют покупки")


@dp.callback_query_handler(text="promo", state="*")
async def active_promo(call: CallbackQuery, state: FSMContext):
    message: types.Message = call.message

    try:
        await message.delete()
    except:
        ...

    await message.answer("<b>💠 Введите промокод</b>: ", reply_markup = on_main)
    await StorageUsers.active_promo.set()

@dp.message_handler(content_types="text", state=StorageUsers.active_promo)
async def write_active_promo(message: types.Message, state: FSMContext):
    name_promo = message.text
    row = await get_storage_promocod(name_promo)
    if not row:
        return await message.answer("😔 Ех, кажись нет, такого промокода")

    procent, count_use = row[0]
    
    count_activete = await get_count_use(name_promo)
    if count_activete >= count_use:
        return await message.answer("😔 Ех, Извиниье, промокод больше недействителен")
    
    res = await get_user_promocod(message.from_user.id, name_promo)
    if res:
        return await message.answer("😔 Вы уже активировали этот промокод")

    await add_user_promocod(name_promo, message.from_user.id, False)
    await message.answer(f"Вы активировали промокод на {procent}%")

    await state.finish()



################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Открытие категории для покупки
@dp.callback_query_handler(text_startswith="buy_open_category", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    get_settings = await get_settingsx()
    if get_settings[3] == "True" or str(call.from_user.id) in admins:
        category_id = int(call.data.split(":")[1])
        get_category = await get_categoryx("*", category_id=category_id)
        get_positions = await get_positionsx("*", category_id=category_id)

        get_kb = await buy_item_item_position_ap(0, category_id, call.from_user.id)
        if len(get_positions) >= 1:
            await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                        call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=get_kb)
        else:
            await bot.answer_callback_query(call.id, f"❕ Товары в категории {get_category[2]} отсутствуют.")
    else:
        await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)


# Вернутсья к предыдущей категории при покупке
@dp.callback_query_handler(text_startswith="back_buy_item_to_category", state="*")
async def back_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    get_kb = await buy_item_open_category_ap(0)

    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def buy_item_next_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    get_kb = await buy_item_next_page_category_ap(remover)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_prevp", state="*")
async def buy_item_prev_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    get_kb = await buy_item_previous_page_category_ap(remover)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Следующая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_kb = await item_buy_next_page_position_ap(remover, category_id)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Предыдущая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_prevp", state="*")
async def buy_item_prev_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_kb = await item_buy_previous_page_position_ap(remover, category_id)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Возвращение к страницам позиций при покупке товара
@dp.callback_query_handler(text_startswith="back_buy_item_position", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_kb = await buy_item_item_position_ap(remover, category_id, call.from_user.id)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id,
                           "<b>🎁 Выберите нужный вам товар:</b>",
                           reply_markup=get_kb)


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_open_position", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    await position(
        call.from_user.id,
        call.data.split(":")[1],
        call.data.split(":")[2],
        call.data.split(":")[3],
        call.message,
        call
    )

@dp.message_handler(IsPrivate(), IsAdmin(), text_startswith="/sell", state="*")
@dp.channel_post_handler(text_startswith="/sell", state="*")
async def sell_item(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except:
        ...

    args = message.text.split('=')
    if len(args) < 2:
        try:
            await bot.send_message(message.from_user.id, "⚠️Мало аргументов для отправки поста")
        except:
            ...
        return
    data = args[1].split(':')
    if len(data) != 3:
        try:
            await bot.send_message(message.from_user.id, "⚠️Количество аргументов != 3")
        except:
            ...
        return

    sPosition_id, sRemover, sCategory_id = data
    
    await position(
        None,
        sPosition_id,
        sRemover,
        sCategory_id,
        message,
        is_sell=True
    )

async def position(
    from_user_id: int, 
    sPosition_id: str, 
    sRemover: str, 
    sCategory_id: str,
    message: types.Message,
    call: CallbackQuery = None,
    *,
    is_sell: bool = False
):
    get_settings = await get_settingsx()
    if not is_sell and get_settings[3] != "True" and str(from_user_id) not in admins:
        if call is None:
            return await message.answer("🔴 Покупки в боте временно отключены.")
        return await call.answer("🔴 Покупки в боте временно отключены.", True)
    
    position_id = int(sPosition_id)
    remover = int(sRemover)
    category_id = int(sCategory_id)

    get_position = await get_positionx("*", position_id=position_id)
    get_category = await get_categoryx("*", category_id=category_id)
    get_items    = await get_itemsx("*", position_id=position_id)
    
    command = ""
    if not is_sell and str(from_user_id) in admins:
        command = f"<b>Command: <code>/sell={sPosition_id}:{sRemover}:{sCategory_id}</code></b>\n"

    cost = get_position[3]
    position_text = f"{cost}"
    if not is_sell:
        count_procent = await get_count_procent(from_user_id)

        if count_procent > 0:
            new_cost = round(cost - (count_procent / 100) * cost, 2)
            if new_cost > 1:
                position_text = f"<del>{cost}</del> {new_cost}"

    send_msg = (
        f"<b>🎁 Покупка товара:</b>\n" + command +
        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" 
        f"<b>📜 Категория:</b> {get_category[2]}\n" 
        f"<b>🏷 Название:</b> {get_position[2]}\n" 
        f"<b>💵 Стоимость:</b> {position_text}$\n" 
        f"<b>📦 Количество:</b> {len(get_items)}шт\n"
        f"<b>📜 Описание:</b>\n"
        f"{get_position[4]}\n"
    )

    if is_sell:
        me = await bot.get_me()
        markup = sell_item_func(
            position_id, 
            remover, 
            category_id,
            me.username
        )
    else:
        markup = open_item_func(
            position_id, 
            remover, 
            category_id
        )

    if is_sell:
        send_msg = f"<b>💵 Стоимость:</b> {position_text}$"

    if len(get_position[5]) >= 5:
        #if is_sell or message.from_user.is_bot:
        #    await message.delete()
        return await message.answer_photo(
            get_position[5],
            send_msg,
            reply_markup = markup
        )

    if not is_sell and message.from_user.is_bot:
        return await message.edit_text(send_msg, reply_markup = markup)
    return await message.answer(send_msg, reply_markup = markup)



# Выбор кол-ва товаров для покупки
@dp.callback_query_handler(text_startswith="buy_this_item", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    get_settings = await get_settingsx()
    if get_settings[3] == "True" or str(call.from_user.id) in admins:
        position_id = int(call.data.split(":")[1])

        get_items = await get_itemsx("*", position_id=position_id)
        get_position = await get_positionx("*", position_id=position_id)
        get_user = await get_userx(user_id=call.from_user.id)
        if len(get_items) >= 1:
            cost = get_position[3]
            position_text = f"{cost}"
            count_procent = await get_count_procent(call.from_user.id)

            if count_procent > 0:
                new_cost = round(cost - (count_procent / 100) * cost, 2)
                if new_cost > 1:
                    position_text = f"<del>{cost}</del> {new_cost}"
                        
            async with state.proxy() as data:
                data["here_cache_position_id"] = position_id
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await StorageUsers.here_input_count_buy_item.set()
            await bot.send_message(call.from_user.id,
                                   f"📦 <b>Введите количество товаров для покупки</b>\n"
                                   f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                   f"🏷 Название товара: {get_position[2]}\n"
                                   f"💵 Стоимость товара: {position_text}$\n"
                                   f"💳 Ваш баланс: {get_user[4]}$\n",
                                   reply_markup=all_back_to_main_default)
        else:
            await bot.answer_callback_query(call.id, "🎁 Товаров нет в наличии.")
    else:
        await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)


# Принятие кол-ва товаров для покупки
@dp.message_handler(IsPrivate(), state=StorageUsers.here_input_count_buy_item)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    get_settings = await get_settingsx()
    if get_settings[3] != "True" and str(message.from_user.id) not in admins:
        return await message.answer("<b>🔴 Покупки в боте временно отключены.</b>")
    async with state.proxy() as data:
        position_id = data["here_cache_position_id"]

    get_items = await get_itemsx("*", position_id=position_id)
    get_position = await get_positionx("*", position_id=position_id)
    get_user = await get_userx(user_id=message.from_user.id)

    if not message.text.isdigit():
        return await message.answer(
            f"<b>❌ Данные были введены неверно.</b>\n"
            f"<b>📦 Введите количество товаров для покупки</b>\n"
            f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
            f"🏷 Название товара: <code>{get_position[2]}</code>\n"
            f"💵 Стоимость товара: <code>{get_position[3]}$</code>\n",
            reply_markup=all_back_to_main_default
        )
    
    get_count = int(message.text)

    if len(get_items) < 1:
        await state.finish()
        return await message.answer(
            "<b>🎁 Товар который вы хотели купить, закончился</b>",
            check_user_out_func(message.from_user.id)
        )

    if 1 > get_count or get_count > len(get_items):
        return await message.answer(
            f"<b>❌ Неверное количество товаров.</b>\n"
            f"<b>📦 Введите количество товаров для покупки</b>\n"
            f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
            f"🏷 Название товара: <code>{get_position[2]}</code>\n"
            f"💵 Стоимость товара: <code>{get_position[3]}$</code>\n",
            reply_markup=all_back_to_main_default
        )
    
    cost = get_position[3]
    text_cost = f"{cost}"
    count_procent = await get_count_procent(message.from_user.id)
    
    amount_pay = cost * get_count
    text_amount_pay = f"{amount_pay}"

    if count_procent > 0:
        new_cost = round(cost - (count_procent / 100) * cost, 2)
        if new_cost > 1:
            new_amount_pay = new_cost * get_count
            text_amount_pay = f"<del>{amount_pay}</del> {new_amount_pay}"
            text_cost = f"<del>{cost}</del> {new_cost}"
        
            cost = new_cost
            amount_pay = new_amount_pay

    if int(get_user[4]) >= amount_pay:
        await state.finish()
        delete_msg = await message.answer(
            "<b>🎁 Товары подготовалены.</b>",
            reply_markup=check_user_out_func(message.from_user.id)
        )

        await message.answer(
            f"🎁 <b>Вы действительно хотите купить товар(ы)?</b>\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"🏷 Название товара: {get_position[2]}\n"
            f"💵 Стоимость товара: {text_cost}$\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"▶ Количество товаров: {get_count}шт\n"
            f"💰 Сумма к покупке: {text_amount_pay}$",
            reply_markup=confirm_buy_items(
                position_id, get_count,
                delete_msg.message_id
            )
        )
    else:
        await message.answer(
            f"<b>❌ Недостаточно средств на счете.</b>\n"
            f"<b>📦 Введите количество товаров для покупки</b>\n"
            f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
            f"🏷 Название товара: <code>{get_position[2]}</code>\n"
            f"💵 Стоимость товара: <code>{get_position[3]}$</code>\n",
            reply_markup=all_back_to_main_default
        )


# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_items", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    message_id = call.data.split(":")[1]
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.delete_message(call.message.chat.id, message_id)
    await bot.send_message(call.from_user.id,
                           "<b>☑ Вы отменили покупку товаров.</b>",
                           reply_markup=check_user_out_func(call.from_user.id))


# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="xbuy_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    get_settings = await get_settingsx()
    if get_settings[3] != "True" and str(call.from_user.id) not in admins:
        return await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)
    
    delete_msg = await bot.send_message(call.from_user.id,
                                        "<b>🔄 Ждите, товары подготавливаются</b>")
    position_id = int(call.data.split(":")[1])
    get_count = int(call.data.split(":")[2])
    message_id = int(call.data.split(":")[3])

    await bot.delete_message(call.message.chat.id, message_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

    get_items = await get_itemsx("*", position_id=position_id)
    get_position = await get_positionx("*", position_id=position_id)
    get_user = await get_userx(user_id=call.from_user.id)

    cost = int(get_position[3])
    count_procent = await get_count_procent(call.from_user.id)

    if 1 > int(get_count) or int(get_count) > len(get_items):
        await state.finish()
        return await bot.send_message(
            call.from_user.id,
            "<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
            check_user_out_func(call.from_user.id)
        )

    amount_pay = cost * get_count

    if count_procent > 0:
        new_cost = round(cost - (count_procent / 100) * cost, 2)
        if new_cost > 1:
            amount_pay = new_cost * get_count

    if int(get_user[4]) < amount_pay:
        return await bot.send_message(call.from_user.id, "<b>❗ На вашем счёте недостаточно средств</b>")
    
    save_items, send_count, split_len = await buy_itemx(get_items, get_count)

    if split_len <= 50:
        split_len = 70
    elif split_len <= 100:
        split_len = 50
    elif split_len <= 150:
        split_len = 30
    elif split_len <= 200:
        split_len = 10
    else:
        split_len = 3

    if get_count != send_count:
        amount_pay = int(get_position[3]) * send_count
        get_count = send_count

    random_number = [random.randint(100000000, 999999999)]
    passwd = list("ABCDEFGHIGKLMNOPQRSTUVYXWZ")
    random.shuffle(passwd)
    random_char = "".join([random.choice(passwd) for x in range(1)])
    receipt = random_char + str(random_number[0])
    buy_time = datetime.datetime.today().replace(microsecond=0)

    await bot.delete_message(call.from_user.id, delete_msg.message_id)

    if len(save_items) <= split_len:
        send_message = "\n".join(save_items)
        await bot.send_message(
            call.from_user.id,
            f"<b>🎁 Ваши товары:</b>\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"{send_message}"
        )
    else:
        await bot.send_message(
            call.from_user.id,
            f"<b>🎁 Ваши товары:</b>\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖"
        )

        save_split_items = split_messages(save_items, split_len)
        for item in save_split_items:
            send_message = "\n".join(item)
            await bot.send_message(call.from_user.id,
                                    send_message)
    save_items = "\n".join(save_items)
    
    
    if count_procent > 0:
        await update_procent(call.from_user.id)

    await add_purchasex(
        call.from_user.id, 
        call.from_user.username, 
        call.from_user.first_name,
        receipt, 
        get_count, 
        amount_pay, 
        get_position[3], 
        get_position[1], 
        get_position[2],
        save_items, 
        get_user[4], 
        int(get_user[4]) - amount_pay, 
        buy_time, int(time.time())
    )

    await update_userx(call.from_user.id, balance=get_user[4] - amount_pay)

    await bot.send_message(
        call.from_user.id,
        f"<b>🎁 Вы успешно купили товар(ы) ✅</b>\n"
        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        f"📃 Чек: <code>#{receipt}</code>\n"
        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
        f"📦 Куплено товаров: <code>{get_count}</code>\n"
        f"💵 Сумма покупки: <code>{amount_pay}$</code>\n"
        f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
        f"🕜 Дата покупки: <code>{buy_time}</code>",
        reply_markup=check_user_out_func(call.from_user.id)
    )
    


async def processing_items(get_items, get_count):
    send_count = 0
    save_items = []
    for select_send_item in get_items:
        if send_count != get_count:
            send_count += 1
            save_items.append(f"{send_count}. <code>{select_send_item[2]}</code>")
            await remove_itemx(item_id=select_send_item[1])
            split_len = len(f"{send_count}. <code>{select_send_item[2]}</code>")
        else:
            break
    return save_items, send_count, split_len
