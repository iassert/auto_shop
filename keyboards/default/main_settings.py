# - *- coding: utf- 8 - *-
from .builder import InlineKeyboardBuilder

from utils.db_api.sqlite import get_settingsx


async def get_settings_func():
    get_settings = await get_settingsx()
    settings_default = InlineKeyboardBuilder(resize_keyboard=True)
    if get_settings[3] == "True":
        status_buy = "🔴 Выключить покупки"
    elif get_settings[3] == "False":
        status_buy = "🟢 Включить покупки"
    if get_settings[2] == "True":
        status_work = "🔴 Отправить на тех. работы"
    elif get_settings[2] == "False":
        status_work = "🟢 Вывести из тех. работ"
    settings_default.row("ℹ Изменить FAQ 🖍", "📕 Изменить контакты 🖍")
    settings_default.row(status_work, status_buy)
    settings_default.row("⬅ На главную")
    return settings_default


settings_back_default = InlineKeyboardBuilder(resize_keyboard=True)
settings_back_default.row("⚙ К настройкам ↩")
