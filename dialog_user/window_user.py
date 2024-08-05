from operator import attrgetter
from aiogram import F
from aiogram.enums import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, ScrollingGroup, Select, Column, Url, Button, WebApp
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialog_user.callback_user import select_vac, dialog_close, vacancies_list, phone_search_click, get_phone_txt, \
    start, contact_administrator_click, get_admin_message, suggest_post_click, suggest_post_cb, suggest_work_cb
from dialog_user.getter_user import vacancies_list_getter, vac_info_getter, get_main_getter, search_byphone_getter, \
    get_number, contact_admin_getter, suggest_post_getter
from dialog_user.state_user import Vacancies, UserMainMenu, SearchPhoneState, ListenUser, Suggest


def vacancies_window_list(**kwargs):
    return Window(
        Format("Вакансии обновлены\n"),
        DynamicMedia('work_pic'),
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
            # Button(text=Format('ПРЕДЛОЖИТЬ в Ленино Главное Крым🏖'),
            #        id='suggest_post_btn',
            #        on_click=suggest_post_click),
            Button(text=Format('РАБОТА! Вакансии по Ленинскому району'),
                   id='vacancies_btn',
                   on_click=vacancies_list),
            Button(text=Format('Поиск по номеру телефона'),
                   id='search_by_phone_btn',
                   on_click=phone_search_click),
            WebApp(text=Const('Магазин Доброцен'), url=Const('https://1385988-ci25991.tw1.ru')),
        ),
        Button(text=Format('Отправить сообщение администратору'),
               id='Admin_message_btn',
               on_click=contact_administrator_click),
        state=UserMainMenu.start,
        getter=get_main_getter,
    )


def search_byphone_window():
    return Window(
        DynamicMedia('search_phone_pic'),
        Format('Введите номер телефона 10 цифр: +7.......начиная с 9-ки\nОжидаю.....'),
        MessageInput(content_types=[ContentType.TEXT], func=get_phone_txt),
        getter=search_byphone_getter,
        state=SearchPhoneState.start,
    )


def get_phone_window():
    return Window(
        Format('{message}'),
        Format('{phones}', when=F['phones']),
        Button(text=Format('Пробуем ещё'),
               id='elif_btn',
               on_click=phone_search_click),
        Button(text=Format('Главное меню'),
               id='main_menu_btn',
               on_click=start),
        getter=get_number,
        state=SearchPhoneState.get_phone_number,
        disable_web_page_preview=True,
        parse_mode='HTML'
    )


def contact_administrator_window():
    return Window(
        DynamicMedia('contact_admin'),
        Const('Админ слушает, принимает к сведению, но не отвечает\nПишите...'),
        MessageInput(content_types=[ContentType.TEXT], func=get_admin_message),
        state=ListenUser.to_admin_,
        getter=contact_admin_getter
    )


def suggest_buttons():
    return Window(
        Button(text=Format('Предложить пост'),
               id='suggest_post_btn',
               on_click=suggest_post_cb),
        Button(text=Format('Добавить объявление о работе'),
               id='suggest_work_btn',
               on_click=suggest_work_cb),
        Const('ВАЖНО!'),
        state=Suggest.suggest_choose,
        getter=None
    )
