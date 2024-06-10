from datetime import datetime

from aiogram_dialog import DialogManager
from sqlalchemy import select, Row, Result

from config import engine
from models import PreModData


async def posts_list_getter(**kwargs):
    query = (select(PreModData.date, PreModData.internal_id, PreModData.source_title, PreModData.text)
             .order_by(PreModData.date.desc()))
    async with engine.scoped_session() as session:
        r: Result = await session.execute(query)
        data = r.fetchall()
    return {
        "posts_list_": data
    }


async def post_info_getter(dialog_manager: DialogManager, **kwargs):
    internal_id = dialog_manager.dialog_data.get('internal_id')
    query = select(PreModData).filter(PreModData.internal_id == internal_id)
    async with engine.scoped_session() as session:
        r = await session.execute(query)
        data = r.scalar()
    return {
        'info': data,
    }
