import asyncio
import json
import os
import re
import time
import urllib.request
from itertools import groupby
from operator import itemgetter
import random

from aiogram.types import Message, URLInputFile, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy import Sequence, select, Result
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot import bot
from config import engine, hv, root_path
from crud import write_data, delete_data
from models import Visitors, Posts, PreModData
from yt_dlp import YoutubeDL, DownloadError

from text_edit import replacer


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
    name = random.randint(1, 100000)
    ydl_opts = {'outtmpl': f'attachments/{name}.mp4',
                'ffmpeg-location': '/usr/bin/ffmpeg',
                'ignore-errors': True,
                }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            formats = list()
            pre_res = ydl.extract_info(video, download=False)
            [formats.append(format_) for format_ in pre_res.get('formats') if (format_.get('height')
                                                                               and format_.get('acodec') != 'none')]
            formats.sort(key=itemgetter('height'))
            for format_ in formats:
                if format_.get('height') in format_quality:
                    ydl_opts['format'] = format_.get('format_id')
                    break
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video)
            title = ydl.prepare_filename(result)
        return title
    except DownloadError as de:
        print('DownloadError', de)


async def post_to_telegram(post: PreModData):
    media_group = MediaGroupBuilder()
    caption = await replacer(text=post.text)
    if post.is_repost:
        repost_place = 'public' if post.repost_source_id < 0 else 'id'
        repost = f"<b> → → → → Р Е П О С Т ↓ ↓ ↓ ↓</b>\n" \
                 f"<a href='https://vk.com/{repost_place}{abs(post.repost_source_id)}'>{post.repost_source_title}</a>\n"
        caption = repost + caption
    caption = f"{caption}\n<a href='https://vk.com/id{post.signer_id}'>" \
              f"   👉  {post.signer_name}</a>" if post.signer_name != 'Анонимно' else f"{caption}"
    send_message_args, send_media_args = dict(), dict()
    send_message_args.update(
        chat_id=hv.tg_chat_id,
        text=caption[:4096],
        parse_mode='HTML',
        disable_web_page_preview=True,
        disable_notification=hv.notification
    )

    if post.attachments_info:
        attachments = json.loads(post.attachments)
        if attachments.get('photo') or attachments.get('video'):
            for key, value in attachments.items():
                if key == 'photo':
                    for photo in attachments.get(key):
                        media_group.add_photo(media=URLInputFile(url=photo.get('big_size')), parse_mode='HTML', )
                        await asyncio.sleep(0.5)
                if key == 'video':
                    for video in attachments.get(key):
                        video_title = await download_video(video=video, format_quality=[426, 480, 640, 360, 720, 852])
                        if video_title:
                            if os.path.getsize(f"{root_path}/{video_title}") < 52400000:
                                media_group.add_video(
                                    media=FSInputFile(path=f"{root_path}/{video_title}"),
                                    parse_mode='HTML',
                                    supports_streaming=True,
                                )
                # if key == 'doc':
                #     doc_builder = MediaGroupBuilder()
                #     filename = attachments.get(key).get('title')
                #     urllib.request.urlretrieve(attachments.get(key).get('link'), f"{root_path}/{filename}")
                #     doc_builder.add_document(media=FSInputFile(path=f"{root_path}/{filename}"))
                #     await asyncio.sleep(0.5)
            media_group.caption = caption
            send_media_args.update(
                chat_id=hv.tg_chat_id,
                disable_notification=hv.notification,
                request_timeout=1000
            )
            if len(caption) < 1024:
                send_media_args.update(media=media_group.build())
                answer = await bot.send_media_group(**send_media_args)
            else:
                media_group.caption = None
                send_media_args.update(media=media_group.build())
                answer = await bot.send_media_group(**send_media_args)
                answer = await bot.send_message(**send_message_args)
        else:
            answer = await bot.send_message(**send_message_args)
    else:
        answer = await bot.send_message(**send_message_args)
    if answer:
        for filename in os.listdir(f"{root_path}/attachments/"):
            file_path = os.path.join(f"{root_path}/attachments/", filename)
            os.remove(file_path)
    data_to_post = {
        'post_id': post.internal_id,
        'time': post.date,
        'group_id': post.source_id,
        'group_name': post.source_title,
        'signer_id': post.signer_id,
        'signer_name': post.signer_name,
        'phone_number': post.phone_number,
        'text': post.text,
        'is_repost': post.is_repost,
        'repost_source_id': post.repost_source_id,
        'repost_source_name': post.repost_source_title,
        'attachments': post.attachments_info,
        'source': post.url,
    }
    async with engine.scoped_session() as session:
        await write_data(session=session, table=Posts, data=data_to_post)
        await delete_data(session=session, table=PreModData, column=PreModData.internal_id, data_id=post.internal_id)
