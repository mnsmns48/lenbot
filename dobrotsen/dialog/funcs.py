from typing import Any, Sequence

from sqlalchemy import Result, select, and_, Row, RowMapping
from config import dobro_engine
from dobrotsen.dobrotsen_model import Dobrotsen


async def get_empty_catalogs() -> list:
    sub = select(Dobrotsen.parent).scalar_subquery()
    async with dobro_engine.scoped_session() as session:
        r: Result = await session.execute(
            select(Dobrotsen.parent).filter(
                and_
                (Dobrotsen.id.in_(sub))).group_by(Dobrotsen.parent).order_by(Dobrotsen.parent))
    return list(r.scalars().all())
