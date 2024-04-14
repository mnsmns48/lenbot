from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dobrotsen.dialog.getters import menu_buttons
from dobrotsen.dialog.states import DobrotsenMenu


async def menu_selected(c: CallbackQuery, widget: Any,
                        dialog_manager: DialogManager, item_id: str):

    dialog_manager.dialog_data['button'] = int(item_id)
    await dialog_manager.switch_to(state=DobrotsenMenu.main)