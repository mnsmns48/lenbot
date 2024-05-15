from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

kb = [
    [KeyboardButton(text='Доброцен', web_app=WebAppInfo(url='https://1385988-ci25991.tw1.ru'))],
    [KeyboardButton(text="Прислать скриншот яндекс погоды")],
    [KeyboardButton(text="Последние гости БОТА")],
    [KeyboardButton(text="Запостить рекламу доброцен")],
    [KeyboardButton(text="Запостить работу")],
]
main_admin = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, is_persistent=True)
