from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Back, ListGroup
from aiogram_dialog.widgets.text import Const, Format

from dialog.callbacks import button1_clicked
from dialog.getters import vacancies_list_getter, window2_get_data
from dialog.states import Vacancies


def vacancies_first():
    return Window(
        ListGroup(
            Button(

            )
        ),

        state=Vacancies.vac_list,
        getter=vacancies_list_getter)


def vacancies_second():
    return Window(
        Format("Hello, {name}!"),
        Format("Something: {something}"),
        Format("User input: {dialog_data[user_input]}"),
        Back(text=Const("Back")),
        state=Vacancies.second,
        getter=window2_get_data
    )
