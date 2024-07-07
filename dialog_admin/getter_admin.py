import json

from dataclasses import dataclass
from datetime import datetime

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from config import root_path
from func import download_video
from models import PreModData, Visitors


@dataclass
class PreModePostList:
    date: datetime
    url: str
    internal_id: int
    source_title: str
    text: str
    attachments_info: str


async def posts_list_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    query = (select(
        PreModData.date,
        PreModData.url,
        PreModData.internal_id,
        PreModData.source_title,
        PreModData.text,
        PreModData.attachments_info,
    ).order_by(PreModData.date.desc()))
    r: Result = await session.execute(query)
    data = r.fetchall()
    result = [PreModePostList(line.date.strftime("%d %H:%M"),
                              line.url,
                              line.internal_id,
                              line.source_title[:8],
                              line.text[:25],
                              line.attachments_info) for line in data]
    return {
        "posts_list_": result
    }


async def post_info_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    video_links = list()
    internal_id = dialog_manager.dialog_data.get('internal_id')
    query = select(PreModData).filter(PreModData.internal_id == internal_id)
    r = await session.execute(query)
    data = r.scalar()
    dialog_manager.dialog_data['full_post_info'] = data
    files = list()
    attache = data.attachments
    if attache:
        attachments = json.loads(data.attachments)
        types = list(attachments.keys())
        for type_ in types:
            if type_ == 'photo':
                for line in attachments.get(type_):
                    files.append(
                        MediaAttachment(type=ContentType.PHOTO,
                                        file_id=MediaId(line.get('preview_size'))))
            if type_ == 'video':
                # for video in attachments.get(type_):
                #     video_title = await download_video(video=video, format_quality=[240])
                #     files.append(
                #         MediaAttachment(type=ContentType.VIDEO,
                #                         path=f"{root_path}/{video_title}"))
                for video in attachments.get(type_):
                    video_links.append(video)
    return {
        'date': data.date.strftime("%d.%m %H:%M"),
        'text': data.text[:900],
        'files': files,
        'signer_id': data.signer_id,
        'info': data,
        'attachments_info': data.attachments_info,
        'videos': ' '.join(video_links) + '\n',
    }


async def send_weather_photo(**kwargs):
    media = MediaAttachment(
        path=f"{root_path}/pic_edit/2.jpg",
        type=ContentType.PHOTO)
    return {
        'weather_photo': media
    }


async def get_guests_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    my_row = str()
    query = select(Visitors.time, Visitors.tg_id, Visitors.tg_username, Visitors.tg_fullname).order_by(
        Visitors.time.desc()).limit(15)
    r: Result = await session.execute(query)
    guests = r.all()
    for line in guests:
        my_row += ''.join([f'{line[0].strftime("%d-%m-%Y %H:%M")} {line[1]} {line[2]} {line[3]}\n'])
    return {
        'guests': my_row
    }
