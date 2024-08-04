from typing import Any

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot import bot
from config import hv
from dialog_user.state_user import Vacancies, UserMainMenu, SearchPhoneState, ListenUser, SuggestPost


async def start(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def select_vac(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, vac_id: str):
    dialog_manager.dialog_data['id'] = int(vac_id)
    await dialog_manager.switch_to(Vacancies.vac_info)


async def dialog_close(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def vacancies_list(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(Vacancies.vac_list, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def phone_search_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(SearchPhoneState.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def get_phone_txt(m: Message, widget: MessageInput, dialog_manager: DialogManager):
    await m.delete()
    dialog_manager.dialog_data["phone_txt"] = m.text
    await dialog_manager.switch_to(SearchPhoneState.get_phone_number, show_mode=ShowMode.DELETE_AND_SEND)


async def contact_administrator_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(ListenUser.to_admin_, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def get_admin_message(m: Message, widget: MessageInput, dialog_manager: DialogManager):
    await m.delete()
    text = f'Сообщение админу:\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})\n\n{m.text}'
    await bot.send_message(chat_id=hv.editor_admin, text=text, parse_mode='MarkdownV2')
    await m.answer('Сообщение администратору отправлено ↗↗↗')
    await dialog_manager.answer_callback()
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def suggest_post_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await c.answer('Временно недоступно')

# async def get_post_from_user(m: Message,
#                              widget: MessageInput,
#                              dialog_manager: DialogManager,
#                              album: list[Message] = None):
#     answer_text = 'Твой пост будет выглядит так:\n'
#     if m.content_type == ContentType.TEXT:
#         text_line = f"{m.text}\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})"
#         print(text_line)
#
#     await dialog_manager.switch_to(SuggestPost.get_data, show_mode=ShowMode.DELETE_AND_SEND)
