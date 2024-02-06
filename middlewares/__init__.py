from aiogram import Dispatcher

from .throttling import Throttling


def setup(dp: Dispatcher):
    dp.middleware.setup(Throttling())
