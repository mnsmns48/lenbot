import asyncio
import logging
import sys

from handlers_admin import register_admin_handlers, admin_
from bot import bot, dp
from commands import commands
from handlers_user import register_user_handlers, user_
from config import engine

from db_models import Base


async def bot_working():
    async with engine.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    await register_admin_handlers()
    await register_user_handlers()
    dp.include_routers(admin_, user_)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)

    try:
        print('bot start')
        await dp.start_polling(bot)

    finally:
        print('bot stop')
        await bot.session.close()


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(bot_working())
    except KeyboardInterrupt:
        print('Script stopped')
