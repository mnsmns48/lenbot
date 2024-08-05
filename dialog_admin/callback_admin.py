import asyncio
import os
from typing import Any

from aiogram.types import CallbackQuery, Message, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot import bot
from config import root_path, hv, engine, _img
from dialog_admin.state_admin import PreModerateStates, AdminMainMenu, MarketingState, ListenAdmin, LoadImage
from func import post_to_telegram
from crud import write_data, delete_data
from models import PreModData, BadPosts
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
    await dialog_manager.start(PreModerateStates.post_list, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.DELETE_AND_SEND)


async def on_delete(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    del_id = dialog_manager.dialog_data['internal_id']
    for_add = dialog_manager.dialog_data['full_post_info']
    data = [for_add.date, for_add.url, for_add.source, for_add.internal_id, for_add.source_id]
    async with engine.scoped_session() as session:
        await write_data(session=session, table=BadPosts, data=data)
        await delete_data(session=session, table=PreModData, column=PreModData.internal_id, data_id=del_id)
    await dialog_manager.switch_to(PreModerateStates.post_list)


async def delete_btn_3min(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    del_id = dialog_manager.dialog_data['internal_id']
    async with engine.scoped_session() as session:
        await delete_data(session=session, table=PreModData, column=PreModData.internal_id, data_id=del_id)
    await dialog_manager.switch_to(PreModerateStates.post_list)


async def on_go_post(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.answer_callback()
    await post_to_telegram(post=dialog_manager.dialog_data['full_post_info'])
    await dialog_manager.start(PreModerateStates.post_list, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.DELETE_AND_SEND)


async def posts_manager_click(c: CallbackQuery, widget: Button,
                              dialog_manager: DialogManager):
    await dialog_manager.start(PreModerateStates.post_list)


async def yandex_weather_click(c: CallbackQuery, widget: Button,
                               dialog_manager: DialogManager):
    await c.answer('Жду скриншот погоды')
    await dialog_manager.start(ListenAdmin.get_weather_screen, show_mode=ShowMode.DELETE_AND_SEND)


async def callback_weather_handler(m: Message, message_input: MessageInput, dialog_manager: DialogManager):
    await m.bot.download(file=m.photo[-1].file_id, destination=f"{root_path}/pic_edit/1.jpg")
    await asyncio.sleep(1)
    await m.delete()
    create_weather()
    await dialog_manager.switch_to(ListenAdmin.send_weather, show_mode=ShowMode.DELETE_AND_SEND)


async def send_weather_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await bot.send_photo(chat_id=hv.tg_chat_id,
                         photo=FSInputFile(f"{root_path}/pic_edit/2.jpg"),
                         disable_notification=hv.notification)
    await c.answer('Выхожу')
    await dialog_manager.done()


async def weather_cancel(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await c.answer('Выхожу')
    await dialog_manager.done()


async def choose_marketing(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(MarketingState.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def send_dobrotsen(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Витрина Доброцена", url="https://t.me/pgtlenino_bot"))
    await bot.send_photo(
        chat_id=hv.tg_chat_id,
        photo=_img.dobrotsen_img,
        disable_notification=hv.notification,
        reply_markup=kb.as_markup()
    )
    await dialog_manager.done()
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def send_lenino_work(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="‍🍳 Вакансии 👨‍🔧", url="https://t.me/pgtlenino_bot"))
    await bot.send_photo(
        chat_id=hv.tg_chat_id,
        photo=_img.work_img,
        disable_notification=hv.notification,
        reply_markup=kb.as_markup()
    )
    await dialog_manager.done()
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def get_guests_click(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AdminMainMenu.visitors)


async def start_main_menu(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def load_image(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=LoadImage.get_image, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.DELETE_AND_SEND)
    await c.answer('Жду картинку')


async def upload_pic(m: Message, message_input: MessageInput, dialog_manager: DialogManager):
    id_photo = m.photo[-1].file_id
    await m.answer('Загружено\nID на сервере Telegram:')
    await m.answer(id_photo)
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)
