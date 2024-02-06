# - *- coding: utf- 8 - *-
async def on_startup(dp):
    import logging
    import filters
    import asyncio
    import middlewares

    logging.basicConfig(level = logging.INFO)
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.crypto_bot       import Executor
    from utils.other_func       import on_startup_notify, update_last_profit, check_update_bot, update_profit
    from utils.set_bot_commands import set_default_commands
    from utils.db_api.sqlite    import create_bdx

    from data.config import ctypro_bot_token

    from aiocryptopay import Networks

    await set_default_commands(dp)
    await on_startup_notify(dp)
    await create_bdx()
    await update_profit()

    ex = Executor(ctypro_bot_token, Networks.TEST_NET)
    ex.start_polling()

    print("~~~~~ Bot was started ~~~~~")
    asyncio.create_task(update_last_profit())
    asyncio.create_task(check_update_bot())


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)

# @slivmens