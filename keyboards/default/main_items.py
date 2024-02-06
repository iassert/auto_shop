# - *- coding: utf- 8 - *-
from .builder import InlineKeyboardBuilder

items_default = InlineKeyboardBuilder(resize_keyboard=True)
items_default.row("🎁 Добавить товары ➕", "🎁 Изменить товары 🖍", "🎁 Удалить товары ❌")
items_default.row("📁 Создать позицию ➕", "📁 Изменить позицию 🖍", "📁 Удалить позиции ❌")
items_default.row("📜 Создать категорию ➕", "📜 Изменить категорию 🖍", "📜 Удалить категории ❌")
items_default.row("⬅ На главную")

items_back_default = InlineKeyboardBuilder(resize_keyboard=True)
items_back_default.row("🎁 К управлению товарами ↩")

skip_send_image_default = InlineKeyboardBuilder(resize_keyboard=True)
skip_send_image_default.row("📸 Пропустить")

cancel_send_image_default = InlineKeyboardBuilder(resize_keyboard=True)
cancel_send_image_default.row("📸 Отменить")

finish_load_items_default = InlineKeyboardBuilder(resize_keyboard=True)
finish_load_items_default.row("📥 Закончить загрузку товаров")
