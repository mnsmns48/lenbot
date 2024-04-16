from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy import select, Result

from config import dobro_engine
from dobrotsen.dialog.funcs import get_empty_catalogs
from dobrotsen.dialog.states import DobrotsenMenu
from dobrotsen.dobrotsen_model import Dobrotsen


async def last_parent_id() -> int:
    async with dobro_engine.scoped_session() as session:
        r: Result = await session.execute(
            select(max(Dobrotsen.id).filter(Dobrotsen.price is None))
        )
    return r.scalar()


async def menu_selected(c: CallbackQuery, widget: Any,
                        dialog_manager: DialogManager, item_id: str, **kwargs):
    # button = dialog_manager.dialog_data.get('button')
    if item_id in await get_empty_catalogs():
        dialog_manager.dialog_data['button'] = item_id
        await dialog_manager.switch_to(state=DobrotsenMenu.walking)
    else:
        dialog_manager.dialog_data['button'] = item_id
        await dialog_manager.switch_to(state=DobrotsenMenu.products)
