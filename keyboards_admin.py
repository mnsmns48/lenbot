from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

kb = [
    [KeyboardButton(text='Менеджер Постов')],
    [KeyboardButton(text="Прислать скриншот яндекс погоды")],
    [KeyboardButton(text="Последние гости БОТА")],
    [KeyboardButton(text="Запостить рекламу доброцен")],
    [KeyboardButton(text="Запостить работу")],
]
main_admin = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, is_persistent=True)

