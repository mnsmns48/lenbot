from aiogram_dialog import Dialog

from dialog.getters import dialog_get_data
from dialog.windows import vacancies_second, vacancies_first

vacancies = Dialog(
    vacancies_first(),
    vacancies_second(),
    getter=dialog_get_data)
