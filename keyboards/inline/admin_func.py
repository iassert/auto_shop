# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..default.builder import InlineKeyboardBuilder

from keyboards.inline.callback_datas import *
from utils.db_api.sqlite import get_paymentx, get_positionx, get_itemsx, get_positionsx, get_categoryx


# Розыгрыш
'''
def give_contest_func(user_id):
    give_contest_kb = InlineKeyboardMarkup()
    give_kb = InlineKeyboardButton(text="✅ Выдать приз",
                                   callback_data=user_give_win_cd.new(
                                       user_id=user_id))
    cancel_kb = InlineKeyboardButton(text="❌ Отменить розыгрыш", callback_data="cancel_win")
    new_kb = InlineKeyboardButton(text="🔃 Выбрать нового", callback_data="new_winner")
    give_contest_kb.add(give_kb, cancel_kb)
    give_contest_kb.add(new_kb)
    return give_contest_kb
'''

# Поиск профиля
def search_profile_func(user_id):
    search_profile = InlineKeyboardBuilder()
    user_purchases_kb = InlineKeyboardButton(
        text="🛒 Покупки",
        callback_data=user_purchases_cd.new(user_id=user_id)
    )
    add_balance_kb = InlineKeyboardButton(
        text="💴 Выдать баланс",
        callback_data=user_add_balance_cd.new(user_id=user_id)
    )
    set_balance_kb = InlineKeyboardButton(
        text="💸 Изменить баланс",
        callback_data=user_set_balance_cd.new(user_id=user_id)
    )
    send_msg_kb = InlineKeyboardButton(
        text="💌 Отправить СМС",
        callback_data=user_send_message_cd.new(user_id=user_id)
    )
    search_profile.add(add_balance_kb, set_balance_kb)
    search_profile.add(user_purchases_kb, send_msg_kb)
    search_profile.row("⬅ На главную")
    return search_profile


# Способы пополнения
async def choice_way_input_payment_func():
    get_payments = await get_paymentx()
    payment_method = InlineKeyboardBuilder()

    if get_payments[4] == "form":
        change_qiwi_form = InlineKeyboardButton(text="✅ По форме", callback_data="...")
    else:
        change_qiwi_form = InlineKeyboardButton(text="❌ По форме", callback_data="change_payment:form")

    if get_payments[4] == "number":
        change_qiwi_number = InlineKeyboardButton(text="✅ По номеру", callback_data="...")
    else:
        change_qiwi_number = InlineKeyboardButton(text="❌ По номеру", callback_data="change_payment:number")

    if get_payments[4] == "nickname":
        change_qiwi_nickname = InlineKeyboardButton(text="✅ По никнейму", callback_data="...")
    else:
        change_qiwi_nickname = InlineKeyboardButton(text="❌ По никнейму", callback_data="change_payment:nickname")

    payment_method.add(change_qiwi_form, change_qiwi_number)
    payment_method.add(change_qiwi_nickname)
    payment_method.row("⬅ На главную")
    return payment_method


# Изменение категории
async def edit_category_func(category_id, remover):
    category_keyboard = InlineKeyboardMarkup()
    get_fat_count = len(await get_positionsx("*", category_id=category_id))
    get_category = await get_categoryx("*", category_id=category_id)

    messages = "<b>📜 Выберите действие с категорией 🖍</b>\n" \
               "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_category[2]}</code>\n" \
               f"📁 Кол-во позиций: <code>{get_fat_count}шт</code>"

    change_name_kb = InlineKeyboardButton(text="🏷 Изменить название",
                                          callback_data=f"category_edit_name:{category_id}:{remover}")
    remove_kb = InlineKeyboardButton(text="❌ Удалить",
                                     callback_data=f"category_remove:{category_id}:{remover}")
    back_category_kb = InlineKeyboardButton("⬅ Вернуться ↩",
                                            callback_data=f"back_category_edit:{remover}")
    category_keyboard.add(change_name_kb, remove_kb)
    category_keyboard.add(back_category_kb)
    return messages, category_keyboard


# Кнопки с удалением категории
def confirm_remove_func(category_id, remover):
    confirm_remove_keyboard = InlineKeyboardBuilder()
    change_name_kb = InlineKeyboardButton(text="❌ Да, удалить",
                                          callback_data=f"yes_remove_category:{category_id}:{remover}")
    move_kb = InlineKeyboardButton(text="✅ Нет, отменить",
                                   callback_data=f"not_remove_category:{category_id}:{remover}")
    confirm_remove_keyboard.add(change_name_kb, move_kb)
    confirm_remove_keyboard.row("⬅ На главную")

    return confirm_remove_keyboard


# Кнопки при открытии позиции для изменения
async def open_edit_position_func(position_id, category_id, remover):
    open_item_keyboard = InlineKeyboardMarkup()
    get_position = await get_positionx("*", position_id=position_id)
    get_items = await get_itemsx("*", position_id=position_id)
    have_photo = False
    photo_text = "Отсутствует ❌"
    if len(get_position[5]) >= 5:
        have_photo = True
        photo_text = "Имеется ✅"
    messages = "📁 <b>Редактирование позиции:</b>\n" \
               "➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 <b>Название:</b> <code>{get_position[2]}</code>\n" \
               f"💵 <b>Стоимость:</b> <code>{get_position[3]}руб</code>\n" \
               f"📦 <b>Количество:</b> <code>{len(get_items)}шт</code>\n" \
               f"📸 <b>Изображение:</b> <code>{photo_text}</code>\n" \
               f"📜 <b>Описание:</b> \n" \
               f"{get_position[4]}\n"
    edit_name_kb = InlineKeyboardButton(text="🏷 Изм. название",
                                        callback_data=f"position_change_name:{position_id}:{category_id}:{remover}")
    edit_price_kb = InlineKeyboardButton(text="💵 Изм. цену",
                                         callback_data=f"position_change_price:{position_id}:{category_id}:{remover}")
    edit_discr_kb = InlineKeyboardButton(text="📜 Изм. описание",
                                         callback_data=f"position_change_discription:{position_id}:{category_id}:{remover}")
    edit_photo_kb = InlineKeyboardButton(text="📸 Изм. фото",
                                         callback_data=f"position_change_photo:{position_id}:{category_id}:{remover}")
    remove_kb = InlineKeyboardButton(text="❌ Удалить",
                                     callback_data=f"position_remove_this:{position_id}:{category_id}:{remover}")
    back_positions_kb = InlineKeyboardButton("⬅ Вернуться ↩",
                                             callback_data=f"back_position_edit:{category_id}:{remover}")
    open_item_keyboard.add(edit_name_kb, edit_price_kb)
    open_item_keyboard.add(edit_discr_kb, edit_photo_kb)
    open_item_keyboard.add(remove_kb, back_positions_kb)
    return messages, open_item_keyboard, have_photo


# Подтверждение удаления позиции
def confirm_remove_position_func(position_id, category_id, remover):
    confirm_remove_position_keyboard = InlineKeyboardBuilder()
    change_name_kb = InlineKeyboardButton(text="❌ Да, удалить",
                                          callback_data=f"yes_remove_position:{position_id}:{category_id}:{remover}")
    move_kb = InlineKeyboardButton(text="✅ Нет, отменить",
                                   callback_data=f"not_remove_position:{position_id}:{category_id}:{remover}")
    confirm_remove_position_keyboard.add(change_name_kb, move_kb)
    confirm_remove_position_keyboard.row("⬅ На главную")
    return confirm_remove_position_keyboard
