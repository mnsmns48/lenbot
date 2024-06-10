from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dialog_premoderate.states_premod import PreModerateStates


async def dialog_close(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()


async def select_post(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, internal_id: str):
    dialog_manager.dialog_data['internal_id'] = int(internal_id)
    await dialog_manager.switch_to(PreModerateStates.post_info)
