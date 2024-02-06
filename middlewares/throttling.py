# - *- coding: utf- 8 - *-
import asyncio

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from datetime import datetime



LAST_ID_KEY       = "last_id"
LAST_DATETIME_KEY = "last_datetime_key"
CUSTOM_DEFAULT_RATE_LIMIT = 0.5


class Throttling(BaseMiddleware):
    __last_update: dict[
        int, dict[
            str, int | datetime
        ]
    ] = {}

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.text:
            return

        from_user_id = message.from_user.id

        current_datetime = datetime.now()
        last_datetime: datetime = Throttling.__last_update.get(from_user_id, {}).get(LAST_DATETIME_KEY)

        Throttling.__last_update[from_user_id] = {
            LAST_ID_KEY: message.message_id,
            LAST_DATETIME_KEY: current_datetime
        }

        if last_datetime is not None:
            diff = (current_datetime - last_datetime).total_seconds()
            if diff <= CUSTOM_DEFAULT_RATE_LIMIT:
                await asyncio.sleep(CUSTOM_DEFAULT_RATE_LIMIT)

                if message.message_id != Throttling.__last_update[from_user_id][LAST_ID_KEY]:
                    raise CancelHandler()

        #raise CancelHandler()

