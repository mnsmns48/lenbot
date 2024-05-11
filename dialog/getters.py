from datetime import datetime

from sqlalchemy import select, Result

from config import engine
from db_models import LeninoWork


async def vacancies_list_getter(**kwargs):
    query = select(LeninoWork).order_by(LeninoWork.updated_at.desc())
    async with engine.scoped_session() as session:
        r = await session.execute(query)
        data = r.scalars()
    return {
        "vacancies_list_getter": data,
    }


async def window2_get_data(**kwargs):
    return {
        "something": "data from Window2 getter",
    }


async def dialog_get_data(**kwargs):
    return {
        "name": "Tishka17",
    }
