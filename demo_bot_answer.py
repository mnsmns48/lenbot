import asyncio

from bot import bot


async def answer():
    await bot.send_message(chat_id='5227482940', text='Доброе утро. Такого функционала на данный момент не предусмотрено. Объявления в колонке РАБОТА берутся из АВИТО. Разместите там и оно "подтянется" в наш канал')


if __name__ == '__main__':
    asyncio.run(answer())
