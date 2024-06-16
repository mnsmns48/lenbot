import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, FSInputFile, InputFile, \
    CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput

from bot import bot
from dialog_admin.dialog_main_premod import admin_main_menu, admin_post_manager, admin_yandex_weather, \
    admin_marketing
from dialog_admin.states_premod import PreModerateStates, AdminMainMenu
from dialog_user.states import Vacancies
from fsm import ListenUser, ListenAdmin
from keyboards_admin import main_admin
from func import last_guests, get_info_by_phone
from config import engine, hv, root_path

from filter import AdminFilter
from keyboards_user import dobrotsen_kb, work_kb
from pic_edit.picture_edit import create_weather

admin_ = Router()
admin_.include_routers(
    admin_main_menu,
    admin_post_manager,
    admin_yandex_weather,
    admin_marketing
)


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMainMenu.start, mode=StartMode.RESET_STACK)


async def upload_pic(m: Message):
    id_photo = m.photo[-1].file_id
    await m.answer('ID на сервере Telegram:')
    await m.answer(id_photo)


async def show_guests(m: Message):
    async with engine.scoped_session() as session:
        answer = await last_guests(session=session)
    await m.answer(text=answer)


async def get_weather(m: Message, state=FSMContext):
    await m.answer(text='Жду скриншот погоды')
    await state.set_state(ListenAdmin.get_weather_screen)
    await m.delete()


async def weather_handler(m: Message, message_input: MessageInput, manager: DialogManager):
    await m.bot.download(file=manager.dialog_data['photo'].photo[-1].file_id, destination=f"{root_path}/pic_edit/1.jpg")
    await asyncio.sleep(1)
    await m.delete()
    result = create_weather()
    if result:
        kb_ = InlineKeyboardBuilder()
        kb_.add(InlineKeyboardButton(
            text='Отправить️',
            callback_data='send_weather')
        )
        kb_.add(InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel')
        )
        await m.answer_photo(FSInputFile(f"{root_path}/pic_edit/2.jpg"),
                             reply_markup=kb_.as_markup())


    else:
        await m.answer('Что-то полшо не так')
        await state.clear()
        await m.delete()


async def weather_answer(c: CallbackQuery, state=FSMContext):
    if c.data == 'cancel':
        await c.answer('Отмена')
        await state.clear()
    if c.data == 'send_weather':
        await c.answer('Отправлено')
        await c.bot.send_photo(chat_id=hv.tg_chat_id,
                               photo=FSInputFile(f"{root_path}/pic_edit/2.jpg"),
                               disable_notification=hv.notification)
    await c.message.delete()


async def send_dobrotsen_marketing(m: Message):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Цены Доброцена", url="https://t.me/pgtlenino_bot"))
    await bot.send_photo(chat_id=hv.tg_chat_id,
                         photo='AgACAgIAAxkBAAIxqGY3PMK0W54gK0l_Xyqe3OaeIpdCAAKR1jEbO1rASUiom6L0TtkgAQADAgADeAADNQQ',
                         disable_notification=hv.notification,
                         reply_markup=kb.as_markup())


async def send_work_marketing(m: Message):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="👨‍🍳 Вакансии 👨‍🔧", url="https://t.me/pgtlenino_bot"))
    await bot.send_photo(chat_id=hv.tg_chat_id,
                         photo='AgACAgIAAxkBAAIzn2ZAikXxLIHIgEjP6CJ905PAUfFmAAI62zEba4MAAUrp7N-ctS2YAgEAAwIAA3kAAzUE',
                         disable_notification=hv.notification,
                         reply_markup=kb.as_markup())


async def posts_dialogs(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(PreModerateStates.post_list, mode=StartMode.RESET_STACK)


async def register_admin_handlers():
    admin_.message.filter(AdminFilter())
    admin_.message.register(start, CommandStart())
    # admin_.message.register(posts_dialogs, F.text == 'Менеджер Постов')
    # admin_.callback_query.register(weather_answer, F.data.in_({'send_weather', 'cancel'}),
    #                                ListenAdmin.get_weather_screen)
    # admin_.message.register(get_weather, F.text == "Прислать скриншот яндекс погоды")
    # admin_.message.register(edit_pic, F.photo, ListenAdmin.get_weather_screen)
    # admin_.message.register(upload_pic, F.photo)
    # admin_.message.register(show_guests, F.text == "Последние гости БОТА")
    # admin_.message.register(send_dobrotsen_marketing, F.text == 'Запостить рекламу доброцен')
    # admin_.message.register(send_work_marketing, F.text == 'Запостить работу')
