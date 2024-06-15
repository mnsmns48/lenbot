import re
from itertools import groupby
from operator import itemgetter
import random

from aiogram.types import Message
from sqlalchemy import insert, Sequence, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from config import engine
from models import Visitors, Posts
from yt_dlp import YoutubeDL, DownloadError


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
        query = select(Posts.phone_number, Posts.signer_name, Posts.signer_id).filter(
            Posts.phone_number == int(f"7{m.text}"))
        async with engine.scoped_session() as session:
            r: Result = await session.execute(query)
            result = r.fetchall()
        if result:
            new_x = [el for el, _ in groupby(result)]
            output_str = str()
            for line in new_x:
                if line[1] == 'Анонимно':
                    return 'Нет такого номера базе'
                output_str += ''.join(f"+{line[0]} ссылка ➡️ <a href='https://vk.com/id{line[2]}'>{line[1]}</a>") + '\n'
            return output_str
        else:
            return 'Нет такого номера базе'
    else:
        return 'Нужно ввести 10 цифр номера телефона без +7'


async def download_video(video: str, format_quality: list) -> str | None:
    name = random.randint(1, 10000)
    ydl_opts = {'outtmpl': f'attachments/{name}.mp4',
                'ffmpeg-location': 'ffmpeg',
                'ignore-errors': True,
                }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            formats = list()
            pre_res = ydl.extract_info(video, download=False)
            [formats.append(format_) for format_ in pre_res.get('formats') if format_.get('height')]
            formats.sort(key=itemgetter('height'))
            for format_ in formats:
                if format_.get('height') in format_quality:
                    ydl_opts['format'] = format_.get('format_id')
                    break
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video)
            title = ydl.prepare_filename(result)
        return title
    except DownloadError:
        print('DownloadError')
