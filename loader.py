# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.bot.api import TelegramAPIServer

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)#, server=TelegramAPIServer.from_base('http://localhost:8081'))
dp = Dispatcher(bot, storage=MemoryStorage())
# @slivmens