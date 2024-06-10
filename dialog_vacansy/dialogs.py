from aiogram_dialog import Dialog
from dialog_vacansy.windows import vacancies_window, info_window

vacancies = Dialog(
    vacancies_window(),
    info_window()
)
