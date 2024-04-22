from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession

from dobrotsen.dobrotsen_model import Dobrotsen


async def main_menu(session: AsyncSession, parent: int):
    sub = select(Dobrotsen.parent).scalar_subquery()
    result_data: Result = await session.execute(select(Dobrotsen).filter(
        and_(Dobrotsen.id.in_(sub), (Dobrotsen.parent == parent))))
    res = result_data.scalars().all()
    result = {'data': res}
    return result


async def walking_menu(session: AsyncSession, parent: int):
    result_data: Result = await session.execute(
        select(Dobrotsen).filter(Dobrotsen.parent == parent).order_by(Dobrotsen.price))
    p: Result = await session.execute(
        select(Dobrotsen.parent).filter(Dobrotsen.id == parent))
    res_p = p.scalars().one()
    res = result_data.scalars().all()
    if res:
        end = True if res[0].price else False
        result = {'data': res, 'end': end, 'parent': res_p if res_p != 0 else ''}
    else:
        result = {'data': None, 'end': None}
    return result
