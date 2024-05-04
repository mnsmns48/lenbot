from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

kb = [
    [KeyboardButton(text="Последние гости")],
    [KeyboardButton(text="Проверь номер телефона")],
    [KeyboardButton(text='W-APP', web_app=WebAppInfo(url='https://1385988-ci25991.tw1.ru'))],
]
main_admin = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, is_persistent=True)
