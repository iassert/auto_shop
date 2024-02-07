# - *- coding: utf- 8 - *-
from .builder import InlineKeyboardBuilder


def get_functions_func(user_id):
    functions_default = InlineKeyboardBuilder(resize_keyboard=True)
    functions_default.row("📱 Поиск профиля 🔍", "📃 Поиск чеков 🔍")
    functions_default.row("📢 Рассылка", "📸 Изменить фото")
    functions_default.row("⬅ На главную")
    return functions_default


functions_back_default = InlineKeyboardBuilder(resize_keyboard=True)
functions_back_default.row("🔆 К общим функциям")
