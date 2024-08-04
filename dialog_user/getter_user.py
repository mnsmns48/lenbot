import re
from datetime import datetime
from itertools import groupby

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from config import engine, hv, _img
from models import LeninoWork, Posts


async def vacancies_list_getter(**kwargs):
    query = select(LeninoWork.id, LeninoWork.title).order_by(LeninoWork.updated_at.desc())
    async with engine.scoped_session() as session:
        r = await session.execute(query)
        data = r.fetchall()
    image_id = _img.work_img
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        "vacancies_list_": data,
        'work_pic': image
    }


async def vac_info_getter(dialog_manager: DialogManager, **kwargs):
    v_id = dialog_manager.dialog_data.get('id')
    query = select(LeninoWork).filter(LeninoWork.id == v_id)
    async with engine.scoped_session() as session:
        r = await session.execute(query)
        data = r.scalar()
    return {
        'info': data,
        'date': datetime.strftime(data.updated_at, "%d.%m.%Y %H:%M"),
    }


async def get_main_getter(**kwargs):
    image_id = _img.main_page_image
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        'main_photo': image
    }


async def search_byphone_getter(**kwargs):
    image_id = _img.search_number
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))

    return {
        'search_phone_pic': image
    }


async def get_number(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    p_number = dialog_manager.dialog_data.get('phone_txt')
    regex = re.search(r'\d{10}', p_number)
    if regex:
        query = select(Posts.phone_number, Posts.signer_name, Posts.signer_id).filter(
            Posts.phone_number == int(f"7{p_number}"))
        r: Result = await session.execute(query)
        result = r.fetchall()
        if result:
            new_x = [el for el, _ in groupby(result)]
            output_str = str()
            for line in new_x:
                if line[1] == 'Анонимно':
                    return {'message': 'Нет такого номера базе'}
                output_str += ''.join(f"+{line[0]} ссылка ➡️ <a href='https://vk.com/id{line[2]}'>{line[1]}</a>") + '\n'
                return {
                    'message': 'Надено:\n',
                    'phones': output_str
                }
        return {
            'message': 'Номер не найден',
        }
    return {
        'message': 'Неверный формат номера',
    }


async def contact_admin_getter(**kwargs):
    image_id = _img.admin_img
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        'contact_admin': image
    }


async def suggest_post_getter(**kwargs):
    image_id = _img.suggest_post
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    text = ('Пиши текст, отправляй вложения\n\n'
            'ВАЖНО!\n'
            'Прислать нужно одним сообщением!\n\n'
            'Если пост содержит фото и/или видеофайл, сначала добавьте эти файлы, '
            'а текст прикрепите, как подпись к ним\n'
            'Допускается до 10 медиафайлов\n\n'
            'Не забудь указать контакт для связи, если это нужно\n\n'
            'Жду пост....')
    return {
        'suggest_posts': image,
        'text': text
    }
