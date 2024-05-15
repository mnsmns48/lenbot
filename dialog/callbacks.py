import asyncio
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from bot import bot
from dialog.states import Vacancies
from keyboards_user import work_kb


async def select_vac(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, vac_id: str):
    dialog_manager.dialog_data['id'] = int(vac_id)
    await dialog_manager.switch_to(Vacancies.vac_info)


async def dialog_close(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()
    await bot.send_photo(chat_id=c.from_user.id,
                         photo='AgACAgIAAxkBAAIzn2ZAikXxLIHIgEjP6CJ905PAUfFmAAI62zEba4MAAUrp7N-ctS2YAgEAAwIAA3kAAzUE',
                         caption='Найди работу в Ленинском районе',
                         reply_markup=work_kb.as_markup()
                         )
