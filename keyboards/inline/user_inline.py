# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..default.builder import InlineKeyboardBuilder

from aiocryptopay.models.invoice import Invoice

# Кнопки при поиске профиля через админ-меню
open_profile_inl = InlineKeyboardBuilder()
input_kb = InlineKeyboardButton(text="💵 Пополнить", callback_data="user_input")
mybuy_kb = InlineKeyboardButton(text="🛒 Мои покупки", callback_data="my_buy")
open_profile_inl.add(input_kb, mybuy_kb)
open_profile_inl.row("⬅ На главную")

on_main = InlineKeyboardBuilder()
on_main.row("⬅ На главную")

# Кнопка с возвратом к профилю
to_profile_inl = InlineKeyboardMarkup()
to_profile_inl.add(InlineKeyboardButton(text="📱 Профиль", callback_data="user_profile"))

def asser_crypto_markup(invoice: Invoice) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(
            text = f"Оплатить {invoice.amount}{invoice.asset}",
            url = invoice.bot_invoice_url
        )
    )
    markup.row("⬅ На главную")
    return markup