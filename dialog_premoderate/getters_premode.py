import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select, Row, Result
from sqlalchemy.ext.asyncio import AsyncSession

from config import root_path
from func import download_video
from models import PreModData


@dataclass
class PreModePostList:
    date: datetime
    internal_id: int
    source_title: str
    text: str
    attachments_info: str


async def posts_list_getter(session: AsyncSession, **kwargs):
    query = (select(PreModData.date,
                    PreModData.internal_id,
                    PreModData.source_title,
                    PreModData.text,
                    PreModData.attachments_info)
             .order_by(PreModData.date.desc()))
    r: Result = await session.execute(query)
    data = r.fetchall()
    result = [PreModePostList(line.date.strftime("%d %H:%M"),
                              line.internal_id,
                              line.source_title[:8],
                              line.text[:25],
                              line.attachments_info) for line in data]
    return {
        "posts_list_": result
    }


async def post_info_getter(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    files_to_del = list()
    internal_id = dialog_manager.dialog_data.get('internal_id')
    query = select(PreModData).filter(PreModData.internal_id == internal_id)
    r = await session.execute(query)
    data = r.scalar()
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
                for video in attachments.get(type_):
                    video_title = await download_video(video=video, format_quality=[240])
                    files.append(
                        MediaAttachment(type=ContentType.VIDEO,
                                        path=f"{root_path}/{video_title}"))
                    files_to_del.append(f"{root_path}/{video_title}")
    return {
        'date': data.date.strftime("%d.%m %H:%M"),
        'text': data.text[:950],
        'files_to_del': files_to_del,
        'files': files,
        'info': data,
        'attachments_info': data.attachments_info
    }
