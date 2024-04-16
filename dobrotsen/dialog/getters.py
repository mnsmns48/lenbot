from aiogram_dialog import DialogManager
from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config import dobro_engine
from dobrotsen.dobrotsen_model import Dobrotsen


# async def main_menu(dialog_manager: DialogManager, **kwargs):
#     button_id = dialog_manager.dialog_data.get('button')
#     if not button_id:
#         button_id = 0
#     async with dobro_engine.scoped_session() as session:
#         sub = select(Dobrotsen.parent).scalar_subquery()
#         result_data: Result = await session.execute(select(Dobrotsen.id, Dobrotsen.title).filter(
#             and_(Dobrotsen.id.in_(sub), (Dobrotsen.parent == button_id))))
#         result_catalog_title: Result = await session.execute(select(Dobrotsen.title).filter(Dobrotsen.id == button_id))
#     response = {'menu': result_data.fetchall()}
#     cat_title = result_catalog_title.scalar()
#     if cat_title:
#         response.update({'catalog': cat_title})
#         return response
#     response.update({'catalog': 'Главное меню'})
#     return response

async def get_catalogs(session: AsyncSession, **kwargs):
    sub = select(Dobrotsen.parent).scalar_subquery()
    result_data: Result = await session.execute(select(Dobrotsen.id, Dobrotsen.title).filter(
        and_(Dobrotsen.id.in_(sub), (Dobrotsen.parent == kwargs.get('parent')))))
    return result_data.fetchall()


async def main_menu(dialog_manager: DialogManager, **kwargs):
    async with dobro_engine.scoped_session() as session:
        result = await get_catalogs(session=session, parent=0)
    return {'menu': result}


async def walking_menu(dialog_manager: DialogManager, **kwargs):
    button_id = dialog_manager.dialog_data.get('button')
    async with dobro_engine.scoped_session() as session:
        result = await get_catalogs(session=session, parent=button_id)
        result_catalog_title: Result = await session.execute(select(Dobrotsen.title)
                                                             .filter(Dobrotsen.id == button_id))
    return {'menu': result,
            'catalog': result_catalog_title.scalar()}


async def show_products(dialog_manager: DialogManager, **kwargs):
    button_id = dialog_manager.dialog_data.get('button')
    async with dobro_engine.scoped_session() as session:
        result = await session.execute(select(Dobrotsen.id, Dobrotsen.title, Dobrotsen.price)
        .filter(Dobrotsen.parent == button_id).order_by(
            Dobrotsen.price))
        result_catalog_title: Result = await session.execute(
            select(Dobrotsen.title).filter(Dobrotsen.id == button_id))
    return {'menu': result.fetchall(),
            'catalog': result_catalog_title.scalar()}
