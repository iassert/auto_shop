# - *- coding: utf- 8 - *-
import datetime
import logging
import random
import time

import aiosqlite

from data.config import bot_description

# Путь к БД
path_to_db = "data/botBD.sqlite"


def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)


def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


####################################################################################################
###################################### ФОРМАТИРОВАНИЕ ЗАПРОСА ######################################
# Форматирование запроса с аргументами
async def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
async def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя
async def add_userx(user_id, user_login, user_name, balance, all_refill, reg_date):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute("INSERT INTO storage_users "
                         "(user_id, user_login, user_name, balance, all_refill, reg_date) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         [user_id, user_login, user_name, balance, all_refill, reg_date])
        await db.commit()


# Изменение пользователя
async def update_userx(user_id, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
        sql, parameters = await update_format_with_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Удаление пользователя
async def delete_userx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_users WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Получение пользователя
async def get_userx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchone()
    return get_response


# Получение пользователей
async def get_usersx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchall()
    return get_response


# Получение всех пользователей
async def get_all_usersx():
    async with aiosqlite.connect(path_to_db) as db:
        get_response = await db.execute("SELECT * FROM storage_users")
        get_response = await get_response.fetchall()
    return get_response


# Получение платежных систем
async def get_paymentx():
    async with aiosqlite.connect(path_to_db) as db:
        get_response = await db.execute("SELECT * FROM storage_payment")
        get_response = await get_response.fetchone()
    return get_response


# Изменение платежных систем
async def update_paymentx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"UPDATE storage_payment SET XXX "
        sql, parameters = await update_format_with_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Получение настроек
async def get_settingsx():
    async with aiosqlite.connect(path_to_db) as db:
        get_response = await db.execute("SELECT * FROM storage_settings")
        get_response = await get_response.fetchone()
    return get_response


# Обновление настроек
async def update_settingsx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"UPDATE storage_settings SET XXX "
        sql, parameters = await update_format_with_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Добавление пополнения в БД
async def add_refillx(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute("INSERT INTO storage_refill "
                         "(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix) "
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         [user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix])
        await db.commit()


# Получение пополнения
async def get_refillx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchone()
    return get_response


# Получение пополнений
async def get_refillsx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchall()
    return get_response


# Получение всех пополнений
async def get_all_refillx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_refill"
        get_response = await db.execute(sql)
        get_response = await get_response.fetchall()
    return get_response


# Добавление категории в БД
async def add_categoryx(category_id, category_name):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute("INSERT INTO storage_category "
                         "(category_id, category_name) "
                         "VALUES (?, ?)",
                         [category_id, category_name])
        await db.commit()


# Изменение категории
async def update_categoryx(category_id, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"UPDATE storage_category SET XXX WHERE category_id = {category_id}"
        sql, parameters = await update_format_with_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Получение категории
async def get_categoryx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_category WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchone()
    return get_response


# Получение категорий
async def get_categoriesx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_category WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchall()
    return get_response


# Получение всех категорий
async def get_all_categoriesx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_category"
        get_response = await db.execute(sql)
        get_response = await get_response.fetchall()
    return get_response


# Очистка категорий
async def clear_categoryx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_category"
        await db.execute(sql)
        await db.commit()


# Удаление товаров
async def remove_categoryx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_category WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Добавление категории в БД
async def add_positionx(position_id, position_name, position_price, position_discription, position_image, position_date,
                        category_id):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute("INSERT INTO storage_position "
                         "(position_id, position_name, position_price, position_discription, position_image, position_date, category_id) "
                         "VALUES (?, ?, ?, ?, ?, ?, ?)",
                         [position_id, position_name, position_price, position_discription, position_image,
                          position_date, category_id])
        await db.commit()


# Изменение позиции
async def update_positionx(position_id, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"UPDATE storage_position SET XXX WHERE position_id = {position_id}"
        sql, parameters = await update_format_with_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Получение категории
async def get_positionx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_position WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchone()
    return get_response


# Получение категорий
async def get_positionsx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_position WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchall()
    return get_response


# Получение всех категорий
async def get_all_positionsx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_position"
        get_response = await db.execute(sql)
        get_response = await get_response.fetchall()
    return get_response


# Очистка категорий
async def clear_positionx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_position"
        await db.execute(sql)
        await db.commit()


# Удаление позиций
async def remove_positionx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_position WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Добавление категории в БД
async def add_itemx(category_id, position_id, get_all_items, user_name, user_id):
    async with aiosqlite.connect(path_to_db) as db:
        for item_data in get_all_items:
            if not item_data.isspace() and item_data is not "":
                item_id = [random.randint(100000, 999999)]
                await db.execute("INSERT INTO storage_item "
                                 "(item_id, item_data, position_id, category_id, creator_id, creator_name, add_date) "
                                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 [item_id[0], item_data, position_id, category_id, user_id, user_name,
                                  datetime.datetime.today().replace(microsecond=0)])
        await db.commit()


# Изменение категории
async def update_itemx(item_id, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"UPDATE storage_item SET XXX WHERE item_id = {item_id}"
        sql, parameters = await update_format_with_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Получение категории
async def get_itemx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_item WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchone()
    return get_response


# Получение категорий
async def get_itemsx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_item WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchall()
    return get_response


# Получение всех категорий
async def get_all_itemsx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_item"
        get_response = await db.execute(sql)
        get_response = await get_response.fetchall()
    return get_response


# Очистка категорий
async def clear_itemx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_item"
        await db.execute(sql)
        await db.commit()


# Удаление товаров
async def remove_itemx(**kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "DELETE FROM storage_item WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        await db.execute(sql, parameters)
        await db.commit()


# Покупка товаров
async def buy_itemx(get_items, get_count):
    async with aiosqlite.connect(path_to_db) as db:
        send_count = 0
        save_items = []
        for select_send_item in get_items:
            if send_count != get_count:
                send_count += 1
                save_items.append(f"{send_count}. <code>{select_send_item[2]}</code>")
                sql, parameters = await get_format_args("DELETE FROM storage_item WHERE ", {"item_id":select_send_item[1]})
                await db.execute(sql, parameters)
                split_len = len(f"{send_count}. <code>{select_send_item[2]}</code>")
            else:
                break
        await db.commit()
    return save_items, send_count, split_len


# Добавление покупки в БД
async def add_purchasex(user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                        item_position_id,
                        item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute("INSERT INTO storage_purchases "
                         "(user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item, item_position_id, "
                         "item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix) "
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         [user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                          item_position_id, item_position_name, item_buy, balance_before, balance_after, buy_date,
                          buy_date_unix])
        await db.commit()


# Получение покупки
async def get_purchasex(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_purchases WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchone()
    return get_response


# Получение покупок
async def get_purchasesx(what_select, **kwargs):
    async with aiosqlite.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_purchases WHERE "
        sql, parameters = await get_format_args(sql, kwargs)
        get_response = await db.execute(sql, parameters)
        get_response = await get_response.fetchall()
    return get_response


# Получение всех покупок
async def get_all_purchasesx():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_purchases"
        get_response = await db.execute(sql)
        get_response = await get_response.fetchall()
    return get_response

async def get_all_invoice():
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT invoice_id FROM invoices"
        get_response = await db.execute(sql)
        get_response = await get_response.fetchall()
    return get_response

async def add_invoice(invoice_id: int):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute(
            "INSERT INTO invoices "
            "(invoice_id)"
            "VALUES (?)",
            [invoice_id]
        )
        await db.commit()

async def del_invoice(invoice_id: int):
    async with aiosqlite.connect(path_to_db) as db:
        await db.execute(
            "DELETE FROM invoices "
            "WHERE invoice_id = ?",
            [invoice_id]
        )
        await db.commit()

async def last_purchasesx(user_id):
    async with aiosqlite.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_purchases WHERE user_id = ? ORDER BY increment DESC LIMIT 10"
        get_response = await db.execute(sql, [user_id])
        get_response = await get_response.fetchall()
    return get_response


# Создание всех таблиц для БД
async def create_bdx():
    async with aiosqlite.connect(path_to_db) as db:
        # Создание БД с хранением данных пользователей
        check_sql = await db.execute("PRAGMA table_info(storage_users)")
        check_sql = await check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 7:
            print("DB was found(1/8)")
        else:
            await db.execute("CREATE TABLE storage_users("
                             "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                             "user_id INTEGER, user_login TEXT, user_name TEXT, "
                             "balance INTEGER, all_refill INTEGER, reg_date TIMESTAMP)")
            print("DB was not found(1/8) | Creating...")

        # Создание БД с хранением данных платежных систем
        check_sql = await db.execute("PRAGMA table_info(storage_payment)")
        check_sql = await check_sql.fetchall()
        check_create_payment = [c for c in check_sql]
        if len(check_create_payment) == 6:
            print("DB was found(2/8)")
        else:
            await db.execute("CREATE TABLE storage_payment("
                             "qiwi_login TEXT, qiwi_token TEXT, "
                             "qiwi_private_key TEXT, qiwi_nickname TEXT, "
                             "way_payment TEXT, status TEXT)")
            await db.execute("INSERT INTO storage_payment("
                             "qiwi_login, qiwi_token, "
                             "qiwi_private_key, qiwi_nickname, "
                             "way_payment, status) "
                             "VALUES (?, ?, ?, ?, ?, ?)",
                             ["None", "None", "None", "None", "form", "False"])
            print("DB was not found(2/8) | Creating...")

        # Создание БД с хранением настроек
        check_sql = await db.execute("PRAGMA table_info(storage_settings)")
        check_sql = await check_sql.fetchall()
        check_create_settings = [c for c in check_sql]
        if len(check_create_settings) == 6:
            print("DB was found(3/8)")
        else:
            await db.execute("CREATE TABLE storage_settings("
                             "contact INTEGER, faq TEXT, "
                             "status TEXT, status_buy TEXT,"
                             "profit_buy TEXT, profit_refill TEXT)")
            sql = "INSERT INTO storage_settings(" \
                  "contact, faq, status, status_buy, profit_buy, profit_refill) " \
                  "VALUES (?, ?, ?, ?, ?, ?)"
            now_unix = int(time.time())
            parameters = ("ℹ Контакты. Измените их в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"{bot_description}",
                          "ℹ Информация. Измените её в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"{bot_description}",
                          "True", "True", now_unix, now_unix)
            await db.execute(sql, parameters)
            print("DB was not found(3/8) | Creating...")

        # Создание БД с хранением пополнений пользователей
        check_sql = await db.execute("PRAGMA table_info(storage_refill)")
        check_sql = await check_sql.fetchall()
        check_create_refill = [c for c in check_sql]
        if len(check_create_refill) == 10:
            print("DB was found(4/8)")
        else:
            await db.execute("CREATE TABLE storage_refill("
                             "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "user_id INTEGER, user_login TEXT, "
                             "user_name TEXT, comment TEXT, "
                             "amount TEXT, receipt TEXT, "
                             "way_pay TEXT, dates TIMESTAMP, "
                             "dates_unix TEXT)")
            print("DB was not found(4/8) | Creating...")

        # Создание БД с хранением категорий
        check_sql = await db.execute("PRAGMA table_info(storage_category)")
        check_sql = await check_sql.fetchall()
        check_create_category = [c for c in check_sql]
        if len(check_create_category) == 3:
            print("DB was found(5/8)")
        else:
            await db.execute("CREATE TABLE storage_category("
                             "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "category_id INTEGER, category_name TEXT)")
            print("DB was not found(5/8) | Creating...")

        # Создание БД с хранением позиций
        check_sql = await db.execute("PRAGMA table_info(storage_position)")
        check_sql = await check_sql.fetchall()
        check_create_position = [c for c in check_sql]
        if len(check_create_position) == 8:
            print("DB was found(6/8)")
        else:
            await db.execute("CREATE TABLE storage_position("
                             "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "position_id INTEGER, position_name TEXT, "
                             "position_price INTEGER, position_discription TEXT,"
                             "position_image TEXT, position_date TIMESTAMP, "
                             "category_id INTEGER)")
            print("DB was not found(6/8) | Creating...")

        # Создание БД с хранением товаров
        check_sql = await db.execute("PRAGMA table_info(storage_item)")
        check_sql = await check_sql.fetchall()
        check_create_item = [c for c in check_sql]
        if len(check_create_item) == 8:
            print("DB was found(7/8)")
        else:
            await db.execute("CREATE TABLE storage_item("
                             "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "item_id INTEGER, item_data TEXT, "
                             "position_id INTEGER, category_id INTEGER, "
                             "creator_id INTEGER, creator_name TEXT, "
                             "add_date TIMESTAMP)")
            print("DB was not found(7/8) | Creating...")

        # Создание БД с хранением покупок
        check_sql = await db.execute("PRAGMA table_info(storage_purchases)")
        check_sql = await check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 15:
            print("DB was found(8/8)")
        else:
            await db.execute("CREATE TABLE storage_purchases("
                             "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "user_id INTEGER, user_login TEXT, "
                             "user_name TEXT, receipt TEXT, "
                             "item_count INTEGER, item_price TEXT, "
                             "item_price_one_item TEXT, item_position_id INTEGER, "
                             "item_position_name TEXT, item_buy TEXT, "
                             "balance_before TEXT, balance_after TEXT, "
                             "buy_date TIMESTAMP, buy_date_unix TEXT)")
            print("DB was not found(8/8) | Creating...")

        # Создание БД с invoices
        check_sql = await db.execute("PRAGMA table_info(invoices)")
        check_sql = await check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 1:
            print("DB was found(9/9)")
        else:
            await db.execute("CREATE TABLE invoices("
                             "invoice_id INTEGER)")
            print("DB was not found(9/9) | Creating...")
        await db.commit()
