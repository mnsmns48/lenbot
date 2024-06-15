import asyncio
import os
from typing import Any

from aiogram.types import CallbackQuery, Message, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from bot import bot
from config import root_path, hv
from dialog_premoderate.states_premod import PreModerateStates, AdminMainMenu, MarketingState
from fsm import ListenAdmin
from models import Visitors
from pic_edit.picture_edit import create_weather


async def dialog_close(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await c.answer('Выхожу')
    await dialog_manager.done()


async def select_post(c: CallbackQuery, widget: Any,
                      dialog_manager: DialogManager,
                      internal_id: str):
    dialog_manager.dialog_data['internal_id'] = int(internal_id)
    await dialog_manager.switch_to(PreModerateStates.post_info)


async def start_list(c: CallbackQuery, widget: Any,
                     dialog_manager: DialogManager):
    await dialog_manager.switch_to(PreModerateStates.post_list)


async def clean_cashe_folder(c: CallbackQuery, widget: Any,
                             dialog_manager: DialogManager):
    for filename in os.listdir(f"{root_path}/attachments"):
        file_path = os.path.join(f"{root_path}/attachments", filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            await bot.send_message(chat_id=hv.editor_admin, text='Ошибка')
    await bot.send_message(chat_id=hv.editor_admin, text='Кэш очищен')


async def posts_manager_click(c: CallbackQuery, widget: Button,
                              dialog_manager: DialogManager):
    await dialog_manager.start(PreModerateStates.post_list)


async def yandex_weather_click(c: CallbackQuery, widget: Button,
                               dialog_manager: DialogManager):
    await c.answer('Жду скриншот погоды')
    await dialog_manager.start(ListenAdmin.get_weather_screen)


async def callback_weather_handler(m: Message, message_input: MessageInput, dialog_manager: DialogManager):
    await m.bot.download(file=m.photo[-1].file_id, destination=f"{root_path}/pic_edit/1.jpg")
    await asyncio.sleep(1)
    await m.delete()
    create_weather()
    await dialog_manager.start(ListenAdmin.send_weather)


async def send_weather_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await bot.send_photo(chat_id=hv.tg_chat_id,
                         photo=FSInputFile(f"{root_path}/pic_edit/2.jpg"),
                         disable_notification=hv.notification)
    await dialog_manager.done()
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)


async def weather_cancel(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)


async def choose_marketing(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(MarketingState.start, mode=StartMode.RESET_STACK)


async def send_dobrotsen(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Цены Доброцена", url="https://t.me/pgtlenino_bot"))
    await bot.send_photo(
        chat_id=hv.tg_chat_id,
        photo='gACAgIAAxkBAAIxqGY3PMK0W54gK0l_Xyqe3OaeIpdCAAKR1jEbO1rASUiom6L0TtkgAQADAgADeAADNQQ',
        disable_notification=hv.notification,
        reply_markup=kb.as_markup()
    )
    await dialog_manager.done()
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)


async def send_lenino_work(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="‍🍳 Вакансии 👨‍🔧", url="https://t.me/pgtlenino_bot"))
    await bot.send_photo(
        chat_id=hv.tg_chat_id,
        photo='AgACAgIAAxkBAAIzn2ZAikXxLIHIgEjP6CJ905PAUfFmAAI62zEba4MAAUrp7N-ctS2YAgEAAwIAA3kAAzUE',
        disable_notification=hv.notification,
        reply_markup=kb.as_markup()
    )
    await dialog_manager.done()
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)


async def get_guests_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager, session: AsyncSession):
    query = select(Visitors).order_by(Visitors.time.desc()).limit(15)
    r: Result = await session.execute(query)
    guests = r.scalars