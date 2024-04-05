import re
from itertools import groupby

from aiogram.types import Message
from sqlalchemy import insert, Sequence, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from config import engine
from db_models import Visitors, Posts


async def write_user(m: Message, session: AsyncSession):
    stmt = insert(Visitors).values(
        id=await session.execute(Sequence('visitors_id_seq')),
        tg_id=m.from_user.id,
        tg_username=m.from_user.username,
        tg_fullname=m.from_user.full_name
    )
    await session.execute(stmt)
    await session.commit()


async def last_guests(session: AsyncSession) -> str:
    query = select(Visitors).order_by(Visitors.time.desc()).limit(10)
    r: Result = await session.execute(query)
    guests = r.scalars().all()
    result = str()
    for line in guests:
        result += f"{line.time.strftime('%d-%m-%Y %H:%M')} {line.tg_id} {line.tg_username} {line.tg_fullname}\n"
    return result


async def get_info_by_phone(m: Message):
    regex = re.search(r'\d{10}', m.text)
    if regex:
        query = select(Posts.phone_number, Posts.signer_name, Posts.signer_id).filter(Posts.phone_number == int(f"7{m.text}"))
        async with engine.scoped_session() as session:
            r: Result = await session.execute(query)
            result = r.fetchall()
        if result:
            new_x = [el for el, _ in groupby(result)]
            output_str = str()
            for line in new_x:
                output_str += ''.join(f"+{line[0]} ссылка ➡️ <a href='https://vk.com/id{line[2]}'>{line[1]}</a>") + '\n'
            return output_str
        else:
            return 'Нет такого номера базе'
    else:
        return 'Нужно ввести 10 цифр номера телефона без +7'
