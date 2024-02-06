# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardButton

from utils.db_api.sqlite import *

from ..default.builder import InlineKeyboardBuilder

count_page = 10


################################################################################################
################################# СТРАНИЦЫ ИЗМЕНЕНИЯ КАТЕГОРИЙ #################################
# Стартовые страницы выбора категории для изменения
async def category_open_edit_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"edit_category_here:{get_categories[a][1]}:{remover}"))
        x += 1
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"edit_catategory_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"edit_catategory_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"edit_catategory_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"edit_catategory_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница выбора категории для изменения
async def category_edit_next_page_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"edit_category_here:{get_categories[a][1]}:{remover}"))
        x += 1
    if remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"edit_catategory_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"edit_catategory_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"edit_catategory_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")

    return keyboard


# Предыдующая страница выбора категории для изменения
async def category_edit_prev_page_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"edit_category_here:{get_categories[a][1]}:{remover}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"edit_catategory_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"edit_catategory_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"edit_catategory_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


################################################################################################
################################### СТРАНИЦЫ СОЗДАНИЯ ПОЗИЦИЙ ##################################
# Стартовые страницы выбора категории для добавления позиции
async def position_open_create_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"create_position_here:{get_categories[a][1]}"))
        x += 1
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > count_page:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"create_position_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница выбора категории для добавления позиции
async def position_create_next_page_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"create_position_here:{get_categories[a][1]}"))
        x += 1
    if remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"create_position_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"create_position_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"create_position_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница выбора категории для добавления позиции
async def position_create_previous_page_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"create_position_here:{get_categories[a][1]}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"create_position_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡", callback_data=f"create_position_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅", callback_data=f"create_position_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


################################################################################################
################################## СТРАНИЦЫ ИЗМЕНЕНИЯ ПОЗИЦИЙ ##################################
########################################### Категории ##########################################
# Стартовые страницы категорий при изменении позиции
async def position_open_edit_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"position_edit_category:{get_categories[a][1]}"))
        x += 1
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_category_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_category_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница категорий при изменении позиции
async def position_edit_next_page_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"position_edit_category:{get_categories[a][1]}"))
        x += 1
    if remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_category_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница категорий при изменении позиции
async def position_edit_previous_page_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"position_edit_category:{get_categories[a][1]}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_category_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для их изменения
async def position_open_edit_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"position_edit:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_positions):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_to_category"))
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница позиций для их изменения
async def position_edit_next_page_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"position_edit:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if remover + count_page >= len(get_positions):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_to_category"))
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница позиций для их изменения
async def position_edit_previous_page_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"position_edit:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_to_category"))
    keyboard.row("⬅ На главную")
    return keyboard


################################################################################################
################################## СТРАНИЦЫ ДОБАВЛЕНИЯ ТОВАРОВ #################################
# Стартовые страницы категорий при добавлении товара
async def item_open_add_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"item_add_category:{get_categories[a][1]}"))
        x += 1
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"add_item_category_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"add_item_category_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"add_item_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"add_item_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница категорий при добавлении товара
async def item_add_next_page_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"item_add_category:{get_categories[a][1]}"))
        x += 1
    if remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"add_item_category_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"add_item_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"add_item_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница категорий при добавлении товара
async def item_add_previous_page_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"item_add_category:{get_categories[a][1]}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"add_item_category_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"add_item_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"add_item_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для добавления товаров
async def position_add_item_position_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"item_add_position:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_positions):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_to_category_add_item"))
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница позиций для добавления товаров
async def position_edit_next_page_position_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"item_add_position:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if remover + count_page >= len(get_positions):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_to_category_add_item"))
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница позиций для добавления товаров
async def position_edit_previous_page_position_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"item_add_position:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"edit_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"edit_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_to_category_add_item"))
    keyboard.row("⬅ На главную")
    return keyboard


################################################################################################
################################## СТРАНИЦЫ ПОКУПКИ ТОВАРОВ #################################
# Стартовые страницы категорий при покупке товара
async def buy_item_open_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"buy_open_category:{get_categories[a][1]}"))
        x += 1
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_category_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_category_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница категорий при покупке товара
async def buy_item_next_page_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"buy_open_category:{get_categories[a][1]}"))
        x += 1
    if remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_category_prevp:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница категорий при покупке товара
async def buy_item_previous_page_category_ap(remover):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_categories = await get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            keyboard.add(InlineKeyboardButton(f"{get_categories[a][2]}",
                                              callback_data=f"buy_open_category:{get_categories[a][1]}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_category_nextp:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_category_nextp:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_category_prevp:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.row("⬅ На главную")
    return keyboard


########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для покупки товаров
async def buy_item_item_position_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"buy_open_position:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_position_nextp:{remover + count_page}:{category_id}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_positions):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_position_prevp:{remover - count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_buy_item_to_category"))
    keyboard.row("⬅ На главную")
    return keyboard


# Следующая страница позиций для покупки товаров
async def item_buy_next_page_position_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"buy_open_position:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if remover + count_page >= len(get_positions):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_position_prevp:{remover - count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_buy_item_to_category"))
    keyboard.row("⬅ На главную")
    return keyboard


# Предыдующая страница позиций для покупки товаров
async def item_buy_previous_page_position_ap(remover, category_id):
    x = 0
    keyboard = InlineKeyboardBuilder()
    get_positions = await get_positionsx("*", category_id=category_id)
    for a in range(remover, len(get_positions)):
        if x < count_page:
            get_items = await get_itemsx("*", position_id=get_positions[a][1])
            keyboard.add(InlineKeyboardButton(f"{get_positions[a][2]} | {get_positions[a][3]}$ | {len(get_items)}шт",
                                              callback_data=f"buy_open_position:{get_positions[a][1]}:{remover}:{category_id}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_position_nextp:{remover + count_page}:{category_id}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_position_nextp:{remover + count_page}:{category_id}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_position_prevp:{remover - count_page}:{category_id}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩",
                                      callback_data=f"back_buy_item_to_category"))
    keyboard.row("⬅ На главную")
    return keyboard
