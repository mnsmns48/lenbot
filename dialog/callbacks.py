from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def button1_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data['user_input'] = 'some data from user, stored in `dialog_data`'
    await manager.next()
