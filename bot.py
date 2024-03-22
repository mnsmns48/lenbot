from aiogram import Bot, Dispatcher

from config import hv

bot = Bot(token=hv.bot_token.get_secret_value())
dp = Dispatcher()
