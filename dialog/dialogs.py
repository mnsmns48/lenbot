from aiogram_dialog import Dialog
from dialog.windows import vacancies_window, info_window

vacancies = Dialog(
    vacancies_window(),
    info_window()
)
