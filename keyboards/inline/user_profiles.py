# - *- coding: utf- 8 - *-
from utils.db_api.sqlite import get_userx, get_purchasesx, get_count_procent


async def get_user_profile(user_id):
    count_procent = await get_count_procent(user_id=user_id)

    get_user = await get_userx(user_id=user_id)
    
    balance = round(get_user[4], 3)

    if get_user is not None:
        get_purchases = await get_purchasesx("*", user_id=user_id)
        count_items = 0
        if len(get_purchases) >= 1:
            for items in get_purchases:
                count_items += int(items[5])
        msg = f"👤 <b>Ваш профиль:</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"🔑 Мой ID: <code>{get_user[1]}</code>\n" \
              f"#️⃣ Логин: <b>@{get_user[2]}</b>\n" \
              f"🗣 Имя: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a>\n" \
              f"🕓 Регистрация: <code>{get_user[6]}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"💵 Баланс: <code>{balance}$</code>\n" \
              f"💠Бонус: <code>{count_procent}%</code>\n"\
              f"💸 Всего пополнено: <code>{get_user[5]}$</code>\n" \
              f"🛒 Куплено товаров: <code>{count_items}шт</code>"
        return msg
    else:
        return None


async def search_user_profile(user_id):
    get_status_user = await get_userx(user_id=user_id)
    if get_status_user is not None:
        get_purchases = await get_purchasesx("*", user_id=user_id)
        count_items = 0
        if len(get_purchases) >= 1:
            for items in get_purchases:
                count_items += int(items[5])
        msg = f"📱 <b>Профиль пользователя:</b> <a href='tg://user?id={get_status_user[1]}'>{get_status_user[3]}</a>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"🔑 ID: <code>{get_status_user[1]}</code>\n" \
              f"👤 Логин: <b>@{get_status_user[2]}</b>\n" \
              f"Ⓜ Имя: <a href='tg://user?id={get_status_user[1]}'>{get_status_user[3]}</a>\n" \
              f"🕜 Регистрация: <code>{get_status_user[6]}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"💳 Баланс: <code>{get_status_user[4]}$</code>\n" \
              f"💵 Всего пополнено: <code>{get_status_user[5]}$</code>\n" \
              f"🎁 Куплено товаров: <code>{count_items}шт</code>\n"
        return msg
    else:
        return None
