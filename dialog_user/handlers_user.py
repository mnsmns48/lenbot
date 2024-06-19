import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager, StartMode, Dialog
from sqlalchemy.ext.asyncio import AsyncSession

from dialog_user.state_user import Vacancies, ListenUser, UserMainMenu
from dialog_user.window_user import vacancies_window_list, vacancies_window_info, user_main_menu_window, \
    search_byphone_window, get_phone_window, contact_administrator_window  # suggest_post_window, accept_post_window
from middleware import MediaGroupMiddleware
from func import get_info_by_phone, write_user
from bot import bot
from keyboards_user import main_kb, public
from config import hv

user_ = Router()

user_.message.middleware(MediaGroupMiddleware())

vacancies = Dialog(vacancies_window_list(), vacancies_window_info())
main_menu_dialog = Dialog(user_main_menu_window())
search_byphone_ = Dialog(search_byphone_window(), get_phone_window())
contact_admin_ = Dialog(contact_administrator_window())
# suggest_post = Dialog(suggest_post_window(), accept_post_window())

user_.include_routers(
    main_menu_dialog,
    vacancies,
    search_byphone_,
    contact_admin_,
    # suggest_post
)


async def start(m: Message, dialog_manager: DialogManager, session: AsyncSession):
    await write_user(m, session)
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK)


def receive_attach(album: MediaGroupBuilder, m: Message) -> MediaGroupBuilder:
    if m.content_type == ContentType.PHOTO:
        album.add_photo(m.photo[-1].file_id, parse_mode='MarkdownV2')
    if m.content_type == ContentType.VIDEO:
        album.add_video(m.video.file_id, parse_mode='MarkdownV2')
    return album


# async def start(m: Message):

#     await m.answer_photo(photo='AgACAgIAAxkBAAITZmQlo77a9vGGy1DlE30EBC652E9-AAIyxjEbbWMpSZgCRTKnxt4VAQADAgADeQADLwQ',
#                          caption='Этот бот принимает посты в телеграм канал @leninocremia',
#                          reply_markup=main_kb.as_markup())
#     await m.answer_photo(photo='AgACAgIAAxkBAAIs2mYQU2B8JEANJKgf8_qVirdNzZ66AALw3TEbFxCBSMq61FIW9Rb4AQADAgADeAADNAQ',
#                          reply_markup=dobrotsen_kb.as_markup())
#     await m.answer_photo(photo='AgACAgIAAxkBAAIsvmYQTycTbAba_FyhsimhFAiVAzlTAALa3TEbFxCBSPmCN7X2pEteAQADAgADeAADNAQ',
#                          caption='Узнать владельца номера телефона ↓ ↓ ↓',
#                          reply_markup=search_phone_kb.as_markup())
#     await m.answer_photo(
#         photo='AgACAgIAAxkBAAIzrGZAjVsEs1tPgOAuzByAY3EAAWqykQACRNsxG2uDAAFKvziH6AABwdK8AQADAgADeQADNQQ',
#         caption='Работа в Ленинском районе',
#         reply_markup=work_kb.as_markup())


async def suggest_post_callback(c: CallbackQuery, state=FSMContext):
    await c.answer(text='📣📣📣📣📣📣📣📣📣📣📣📣')
    await state.set_state(ListenUser.suggest_)
    await c.message.answer(text='Пиши текст, отправляй вложения\n\n'
                                'ВАЖНО!\n'
                                'Прислать нужно одним сообщением!\n\n'
                                'Если пост содержит фото и/или видеофайл, сначала добавьте эти файлы, '
                                'а текст прикрепите, как подпись к ним\n'
                                'Допускается до 10 медиафайлов\n\n'
                                'Не забудь указать контакт для связи, если это нужно\n\n'
                                'Жду пост....')


async def to_admin_callback(c: CallbackQuery, state=FSMContext):
    await c.answer(text='Слушаю вас.....')
    await state.set_state(ListenUser.to_admin_)
    await c.message.answer(text='АДМИН этого канала готов выслушать все предложения и пожелания')


async def to_admin(m: Message, state: FSMContext):
    text = (f'Сообщение админу:\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})\n\n{m.text}')
    await bot.send_message(chat_id=hv.tg_bot_admin[0], text=text, parse_mode='MarkdownV2')
    await m.answer('Сообщение админу отправлено\n'
                   'Он скоро прочтёт его. До свидания', reply_markup=main_kb.as_markup())
    await state.clear()


async def suggest_post(m: Message, state: FSMContext, album: list[Message] = None) -> Message:
    answer_text = 'Твой пост будет выглядит так:\n'
    if m.content_type == ContentType.TEXT:
        text_line = f"{m.text}\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})"
        await m.answer(text=f"{answer_text}\n\n{text_line}", parse_mode='MarkdownV2')
        await state.update_data(only_text=text_line)
        return await m.answer("Публикуем? Ожидаю ответ...", reply_markup=public.as_markup())
    album_builder = MediaGroupBuilder(
        caption=f"{m.caption}\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})"
    )
    response = receive_attach(album=album_builder, m=m)
    if album:
        for i in range(1, len(album)):
            response.build().append(receive_attach(album=response, m=album[i]))
    await m.answer(f"{answer_text}")
    await m.answer_media_group(response.build())
    await state.update_data(media_group=response)
    return await m.answer("Публикуем? Ожидаю ответ...", reply_markup=public.as_markup())


async def callback_handler_public(c: CallbackQuery, state=FSMContext):
    await c.answer(text='Пост отправлен администратору на модерацию')
    data_in_state = await state.get_data()
    await bot.send_message(chat_id=hv.tg_bot_admin[0], text='!!!!!!!!!!Пост!!!!!!\n')
    if data_in_state.get('only_text'):
        await bot.send_message(chat_id=hv.tg_bot_admin[0],
                               text=data_in_state.get('only_text'), parse_mode='MarkdownV2')
    else:
        await bot.send_media_group(chat_id=hv.tg_bot_admin[0], media=data_in_state.get('media_group').build())
    await c.message.answer('Отправлено. Ожидайте публикации')
    return await state.clear()


async def callback_handler_again(c: CallbackQuery, state=FSMContext):
    await c.answer('Отмена')
    await c.message.answer('Вы отменили ваш пост, добавьте его заново', reply_markup=main_kb.as_markup())
    await state.clear()


async def test(c: CallbackQuery):
    await c.answer('Получил')
    await c.message.answer('!!!!!!!!!!!!!!')


async def show_phone(c: CallbackQuery, state=FSMContext):
    await c.answer('Загрузка БАЗЫ ДАННЫХ номеров')
    await c.message.answer('Введите номер телефона 10 цифр: +7.......начиная с 9-ки\nОжидаю.....')
    await state.set_state(ListenUser.search_phone)


async def show_phone_m(m: Message, state=FSMContext):
    await m.answer('Введите номер телефона 10 цифр: +7.......начиная с 9-ки\nОжидаю.....')
    await state.set_state(ListenUser.search_phone)


async def take_phone_numb(m: Message, state=FSMContext):
    r = await get_info_by_phone(m)
    await m.answer(r, parse_mode='HTML', disable_web_page_preview=True)
    await state.clear()


async def vacancies_dialogs(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Vacancies.vac_list, mode=StartMode.RESET_STACK)


async def register_user_handlers():
    user_.message.register(start, CommandStart())
    # user_.message.register(show_phone_m, Command("search_phone"))
    # user_.callback_query.register(show_phone, F.data == 'search_phone')
    # user_.callback_query.register(vacancies_dialogs, F.data == 'vacancies')
    # user_.message.register(take_phone_numb, ListenUser.search_phone)
    # user_.callback_query.register(suggest_post_callback, F.data == 'suggest')
    # user_.callback_query.register(to_admin_callback, F.data == 'to_admin')
    # user_.message.register(to_admin, ListenUser.to_admin_)
    # user_.message.register(suggest_post, ListenUser.suggest_)
    # user_.callback_query.register(callback_handler_public, F.data == 'public')
    # user_.callback_query.register(callback_handler_again, F.data == 'again')
