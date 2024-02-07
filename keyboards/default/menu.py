# - *- coding: utf- 8 - *-
from .builder import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins


def check_user_out_func(user_id):
    menu_default = InlineKeyboardBuilder(resize_keyboard=True)
    menu_default.row("💳 Купить", "ℹ FAQ")
    menu_default.row(
        InlineKeyboardButton(text="➕ Пополнить", callback_data="user_input"),
        InlineKeyboardButton(text="💰 Мои покупки", callback_data="my_buy"),
        InlineKeyboardButton(text="💠 Промокод", callback_data="promo")
    )
    menu_default.row("💬 Поддержка")
    if str(user_id) in admins:
        menu_default.row("🎁 Управление товарами 🖍", "📰 Информация о боте")
        menu_default.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
    return menu_default


all_back_to_main_default = InlineKeyboardBuilder(resize_keyboard=True)
all_back_to_main_default.row("⬅ На главную")
