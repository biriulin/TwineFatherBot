from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(token=config.TOKEN_TWINE_FATHER)
dp = Dispatcher(bot, storage=MemoryStorage())
