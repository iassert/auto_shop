# - *- coding: utf- 8 - *-
from .builder import InlineKeyboardBuilder

from utils.db_api.sqlite import get_paymentx


async def payment_default():
    payment = await get_paymentx()
    payment_kb = InlineKeyboardBuilder(resize_keyboard=True)
    payment_kb.row("🥝 Изменить QIWI 🖍", "🥝 Проверить QIWI ♻", "🥝 Баланс QIWI 👁")
    if payment[5] == "True":
        payment_kb.row("🔴 Выключить пополнения")
    else:
        payment_kb.row("🟢 Включить пополнения")
    return payment_kb


payment_back_default = InlineKeyboardBuilder(resize_keyboard=True)
payment_back_default.row("🔑 К платёжным системам ↩")
