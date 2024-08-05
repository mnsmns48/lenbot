import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType, InputMediaPhoto, InputMediaVideo
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager, StartMode, Dialog, ShowMode
from sqlalchemy.ext.asyncio import AsyncSession

from dialog_user.keyboards_user import public, main_kb
from dialog_user.state_user import Vacancies, ListenUser, UserMainMenu, Suggest
from dialog_user.window_user import vacancies_window_list, vacancies_window_info, user_main_menu_window, \
    search_byphone_window, get_phone_window, contact_administrator_window, \
    suggest_buttons
from middleware import AlbumMiddleware
from func import get_info_by_phone, write_user
from bot import bot
from config import hv

user_ = Router()

user_.message.middleware(AlbumMiddleware())

vacancies = Dialog(vacancies_window_list(), vacancies_window_info())
main_menu_dialog = Dialog(user_main_menu_window())
search_byphone_ = Dialog(search_byphone_window(), get_phone_window())
contact_admin_ = Dialog(contact_administrator_window())
suggest = Dialog(suggest_buttons())

user_.include_routers(
    main_menu_dialog,
    vacancies,
    search_byphone_,
    contact_admin_,
    suggest)


async def start(m: Message, dialog_manager: DialogManager, session: AsyncSession):
    await write_user(m, session)
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK)


def receive_attach(album: MediaGroupBuilder, m: Message) -> MediaGroupBuilder:
    if m.content_type == ContentType.PHOTO:
        album.add_photo(m.photo[-1].file_id, parse_mode='MarkdownV2')
    if m.content_type == ContentType.VIDEO:
        album.add_video(m.video.file_id, parse_mode='MarkdownV2')
    return album


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


async def suggest_post(m: Message, state: FSMContext, album: list[Message] = None):
    display_post = 'Твой пост будет выглядит так:\n'
    author_line = f"_{m.text}_\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})"
    if m.caption:
        await state.update_data({'caption': m.caption[:1024]})
    if album:
        for obj in album:
            media = list()
            data = await state.get_data()
            if obj.content_type == ContentType.PHOTO:
                media = InputMediaPhoto(media=obj.photo[-1].file_id)
            if obj.content_type == ContentType.VIDEO:
                media = InputMediaVideo(media=obj.video.file_id)
            data['media'] = data.get('media', []) + [media]
            await state.update_data(data)
        data = await state.get_data()
        if len(data.get('media')) > 1:
            caption = data.get('caption')
            mg = {'media': data['media'], 'caption': caption if caption else ' '}
            media_group = MediaGroupBuilder(media=data['media'], caption=caption if caption else ' ')
            await state.update_data({'type': 'mg', 'data': mg})
            await m.answer(display_post)
            await m.answer_media_group(media_group.build())
            await m.answer("Публикуем? Ожидаю ответ...", reply_markup=public.as_markup())
            await state.set_state(Suggest.publish_post)
    else:
        if m.content_type == ContentType.TEXT:
            answer_text = f"{display_post}\n{author_line}"
            await state.update_data({'type': 'only_text', 'data': author_line})
            await m.answer(answer_text, parse_mode='MarkdownV2')
            await m.answer("Публикуем? Ожидаю ответ...", reply_markup=public.as_markup())
            await state.set_state(Suggest.publish_post)
        if m.content_type == ContentType.PHOTO:
            author_line = f"_{m.caption if m.caption else ' '}_\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})"
            photo = {'media': m.photo[-1].file_id, 'caption': author_line}
            await state.update_data({'type': 'one_photo', 'data': photo})
            await m.answer(display_post)
            await m.answer_photo(photo=photo['media'], caption=photo['caption'], parse_mode='MarkdownV2')
            await m.answer("Публикуем? Ожидаю ответ...", reply_markup=public.as_markup())
            await state.set_state(Suggest.publish_post)
        if m.content_type == ContentType.VIDEO:
            author_line = f"_{m.caption if m.caption else ' '}_\n\nАвтор: [{m.from_user.full_name}](tg://user?id={m.from_user.id})"
            video = {'media': m.video.file_id, 'caption': author_line}
            await state.update_data({'type': 'one_video', 'data': video})
            await m.answer(display_post)
            await m.answer_video(video=video['media'], caption=video['caption'], parse_mode='MarkdownV2')
            await m.answer("Публикуем? Ожидаю ответ...", reply_markup=public.as_markup())
            await state.set_state(Suggest.publish_post)


async def callback_handler_public(c: CallbackQuery, dialog_manager: DialogManager, state=FSMContext):
    if c.data == 'again':
        pass
    if c.data == 'public':
        await c.answer(text='Пост отправлен администратору на модерацию')
        data = await state.get_data()
        if data.get('type') == 'one_video':
            await bot.send_video(chat_id=hv.tg_bot_admin[0],
                                 video=data['data']['media'],
                                 caption=data['data']['caption'],
                                 parse_mode='MarkdownV2')
            await c.message.answer('Отправлено на премодерацию')
        if data.get('type') == 'one_photo':
            await bot.send_photo(chat_id=hv.tg_bot_admin[0],
                                 photo=data['data']['media'],
                                 caption=data['data']['caption'],
                                 parse_mode='MarkdownV2')
            await c.message.answer('Отправлено на премодерацию')
        if data.get('type') == 'only_text':
            await bot.send_message(chat_id=hv.tg_bot_admin[0],
                                   text=data['data'],
                                   parse_mode='MarkdownV2')
            await c.message.answer('Отправлено на премодерацию')
        if data.get('type') == 'mg':
            media_group = MediaGroupBuilder(media=data['data']['media'], caption=data['data']['caption'])
            await bot.send_media_group(chat_id=hv.tg_bot_admin[0],
                                       media=media_group.build())
            await c.message.answer('Отправлено на премодерацию')
    await state.clear()
    await asyncio.sleep(2)
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def callback_handler_again(c: CallbackQuery, dialog_manager: DialogManager, state=FSMContext):
    await c.answer('Отмена')
    await c.message.answer('Вы нажали отмена.\n\nОткрываю главное меню')
    await state.clear()
    await asyncio.sleep(2)
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


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
    user_.message.register(suggest_post, Suggest.suggest_post)
    user_.callback_query.register(callback_handler_again, F.data == 'cancel')
    user_.callback_query.register(callback_handler_public, Suggest.publish_post)
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
