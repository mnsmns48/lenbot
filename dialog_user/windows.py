from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, ScrollingGroup, Select, Column, Url, Cancel, Button
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialog_user.callbacks import select_vac, dialog_close
from dialog_user.getters import vacancies_list_getter, vac_info_getter
from dialog_user.states import Vacancies


def vacancies_window(**kwargs):
    return Window(
        Const("..........................................................................."),
        ScrollingGroup(
            Select(
                Format(text="{item.title}"),
                id='button',
                item_id_getter=attrgetter('id'),
                items='vacancies_list_',
                on_click=select_vac
            ),
            id='main',
            width=1,
            height=8,
            hide_on_single_page=True
        ),
        Button(Const(" -- Выход -- "),
               id="btn",
               on_click=dialog_close),
        state=Vacancies.vac_list,
        getter=vacancies_list_getter
    )


def info_window(**kwargs):
    return Window(
        Multi(
            Format("Вакансия: {info.title}"),
            Format("Обновлено: {date}"),
            Format("Автор объявления: {info.author}"),
            Format("Адрес: {info.locality}"),
            Format("Зарплата: {info.payment}"),
            Format("Условия: {info.cond}"),
            Format("\nОписание: {info.desc}")),
        Url(
            Format("Связаться с автором"),
            Format("{info.link}"),
        ),
        Column(Back(Const("<< Назад к списку вакансий"))),
        state=Vacancies.vac_info,
        getter=vac_info_getter
    )
