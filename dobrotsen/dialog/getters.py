from aiogram_dialog import DialogManager
from sqlalchemy import select, Result, and_

from config import dobro_engine
from dobrotsen.dobrotsen_adv import construct_dobrotsen_menu_kb
from dobrotsen.dobrotsen_model import Dobrotsen


async def menu_buttons(dialog_manager: DialogManager, **kwargs):
    button_id = dialog_manager.dialog_data.get('button')
    if not button_id:
        button_id = 0
    async with dobro_engine.scoped_session() as session:
        sub = select(Dobrotsen.parent).scalar_subquery()
        result: Result = await session.execute(select(Dobrotsen.id, Dobrotsen.title, Dobrotsen.price)
                                               .filter(and_(Dobrotsen.id.in_(sub), (Dobrotsen.parent == button_id))))
    buttons = result.fetchall()
    return {'menu': buttons}