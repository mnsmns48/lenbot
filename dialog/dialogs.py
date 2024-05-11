from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

vacancies = Dialog(
    Window(
        Const('Список вакансий')
    )
)
