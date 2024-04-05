from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = [
    [KeyboardButton(text="Последние гости")],
    [KeyboardButton(text="Проверь номер телефона")],
]
main_admin = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, is_persistent=True)
