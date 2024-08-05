import asyncio
import logging.config
import sys

from aiogram.types import BotCommand

from dialog_admin.handlers_admin import register_admin_handlers, admin_
from bot import bot, dp
from dialog_user.handlers_user import register_user_handlers, user_
from config import engine
from logger import logger


from models import Base

commands = [BotCommand(command='start', description='Главное меню / Перезагрузить бота')]


async def bot_working():
    async with engine.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    await register_admin_handlers()
    await register_user_handlers()
    dp.include_routers(admin_, user_)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)

    try:
        logger.info('bot start')
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    finally:
        logger.info('bot stop')
        await bot.session.close()


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(bot_working())
    except KeyboardInterrupt:
        logger.info('Script stopped')
