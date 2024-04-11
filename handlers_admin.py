import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dobrotsen.dialogs import dialog, MySG
from fsm import ListenUser
from keyboards_admin import main_admin
from db_func import last_guests, get_info_by_phone
from config import engine

from filter import AdminFilter

admin_ = Router()
admin_.include_router(dialog)


async def start(m: Message):
    await m.answer('Admin Mode', reply_markup=main_admin)


async def upload_pic(m: Message):
    id_photo = m.photo[-1].file_id
    await m.answer('ID на сервере Telegram:')
    await m.answer(id_photo)


async def show_guests(m: Message):
    async with engine.scoped_session() as session:
        answer = await last_guests(session=session)
    await m.answer(text=answer)


async def show_phone(m: Message, state=FSMContext):
    await m.answer('Введите номер телефона 10 цифр: +7.......')
    await m.answer('Ожидаю.....')
    await state.set_state(ListenUser.search_phone)


async def take_phone_numb(m: Message, state=FSMContext):
    r = await get_info_by_phone(m)
    await m.answer(r, parse_mode='HTML', disable_web_page_preview=True)
    await state.clear()


async def menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.dialog, mode=StartMode.RESET_STACK)


async def register_admin_handlers():
    admin_.message.filter(AdminFilter())
    admin_.message.register(start, CommandStart())
    admin_.message.register(upload_pic, F.photo)
    admin_.message.register(show_guests, F.text == "Последние гости")
    admin_.message.register(show_phone, F.text == "Проверь номер телефона")
    admin_.message.register(take_phone_numb, ListenUser.search_phone)
    admin_.message.register(menu, Command("menu"))
