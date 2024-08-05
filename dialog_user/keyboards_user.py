from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


main_kb = InlineKeyboardBuilder()
main_kb.add(InlineKeyboardButton(
    text='Предложить пост📝',
    callback_data='suggest')
)
main_kb.add(InlineKeyboardButton(
    text='Написать админу👨🏻‍💼',
    callback_data='to_admin')
)

public = InlineKeyboardBuilder()
public.add(InlineKeyboardButton(
    text='Редактировать🛠️',
    callback_data='again')
)
public.add(InlineKeyboardButton(
    text='Опубликовать🚀',
    callback_data='public')
)

dobrotsen_kb = InlineKeyboardBuilder()
dobrotsen_kb.add(InlineKeyboardButton(
    text='Цены Доброцена',
    web_app=WebAppInfo(url="https://1385988-ci25991.tw1.ru")))

search_phone_kb = InlineKeyboardBuilder()
search_phone_kb.add(InlineKeyboardButton(
    text='Проверка номера',
    callback_data='search_phone'))

work_kb = InlineKeyboardBuilder()
work_kb.add(InlineKeyboardButton(
    text='Список вакансий',
    callback_data='vacancies'
))
