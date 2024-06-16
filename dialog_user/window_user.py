from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, ScrollingGroup, Select, Column, Url, Button, WebApp
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialog_user.callback_user import select_vac, dialog_close, vacancies_list
from dialog_user.getter_user import vacancies_list_getter, vac_info_getter, get_main_getter
from dialog_user.state_user import Vacancies, UserMainMenu


def vacancies_window_list(**kwargs):
    return Window(
        Format("Вакансии обновлены\n"),
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


def vacancies_window_info(**kwargs):
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


def user_main_menu_window(**kwargs):
    return Window(
        Const('Главное меню'),
        DynamicMedia('main_photo'),
        Column(
            Button(text=Format('Предложить пост Ленино Главное Крым🏖'),
                   id='suggest_post_btn',
                   on_click=None),
            Button(text=Format('Работа! Вакансии по Ленинскому району'),
                   id='vacancies_btn',
                   on_click=vacancies_list),
            Button(text=Format('Поиск по номеру телефона'),
                   id='search_by_phone_btn',
                   on_click=None),
            WebApp(text=Const('Магазин Доброцен'), url=Const('https://1385988-ci25991.tw1.ru')),
            Button(text=Format('Отправить сообщение Администратору'),
                   id='Admin_message_btn',
                   on_click=None),
        ),
        state=UserMainMenu.start,
        getter=get_main_getter,
    )
