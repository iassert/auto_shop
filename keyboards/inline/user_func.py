# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..default.builder import InlineKeyboardBuilder

from loader import bot

# Проверка оплаты битка
def create_pay_qiwi_func(send_requests, receipt, message_id, way):
    check_qiwi_pay_inl = InlineKeyboardBuilder()
    check_qiwi_pay_inl.add(InlineKeyboardButton(text="🌀 Перейти к оплате", url=send_requests))
    check_qiwi_pay_inl.add(InlineKeyboardButton(text="🔄 Проверить оплату",
                                                callback_data=f"Pay:{way}:{receipt}:{message_id}"))
    check_qiwi_pay_inl.row("⬅ На главную")
    return check_qiwi_pay_inl


# Кнопки при открытии самого товара
def open_item_func(position_id, remover, category_id):
    open_item = InlineKeyboardMarkup()
    open_item.add(InlineKeyboardButton(
        text="💰 Купить товар",
        callback_data=f"buy_this_item:{position_id}"
    ))
    open_item.add(InlineKeyboardButton(
        text="⬅ Вернуться ↩",
        callback_data=f"back_buy_item_position:{remover}:{category_id}"
    ))
    return open_item

def sell_item_func(
    sPosition_id: str, 
    sRemover: str, 
    sCategory_id: str, 
    username: str
):
    open_item = InlineKeyboardMarkup()
    open_item.add(InlineKeyboardButton(
        text="💰 Купить товар",
        url=f"https://t.me/{username}?start={sPosition_id}_{sRemover}_{sCategory_id}"
    ))

    return open_item

# Подтверждение покупки товара
def confirm_buy_items(position_id, get_count, message_id):
    confirm_buy_item_keyboard = InlineKeyboardMarkup()
    yes_buy_kb = InlineKeyboardButton(text="✅ Подтвердить",
                                      callback_data=f"xbuy_item:{position_id}:{get_count}:{message_id}")
    not_buy_kb = InlineKeyboardButton("❌ Отменить",
                                      callback_data=f"not_buy_items:{message_id}")
    confirm_buy_item_keyboard.add(yes_buy_kb, not_buy_kb)
    return confirm_buy_item_keyboard
