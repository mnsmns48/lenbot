from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import hv

storage = MemoryStorage()
bot = Bot(token=hv.bot_token.get_secret_value())
dp = Dispatcher(storage=storage)
