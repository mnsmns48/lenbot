from datetime import datetime

from aiogram_dialog import DialogManager
from sqlalchemy import select

from config import engine
from models import LeninoWork


async def vacancies_list_getter(**kwargs):
    query = select(LeninoWork.id, LeninoWork.title).order_by(LeninoWork.updated_at.desc())
    async with engine.scoped_session() as session:
        r = await session.execute(query)
        data = r.fetchall()
    return {
        "vacancies_list_": data
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
