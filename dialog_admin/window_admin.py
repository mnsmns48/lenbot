from operator import attrgetter

from aiogram import F
from aiogram.enums import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Column, Url, NumberedPager, Row, WebApp
from aiogram_dialog.widgets.media import MediaScroll, DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialog_admin.callback_admin import dialog_close, select_post, start_list, clean_cashe_folder, \
    posts_manager_click, yandex_weather_click, callback_weather_handler, send_weather_click, choose_marketing, \
    send_dobrotsen, send_lenino_work, weather_cancel, get_guests_click, start_main_menu, on_delete, on_go_post
from dialog_admin.getter_admin import posts_list_getter, post_info_getter, send_weather_photo, \
    get_guests_getter
from dialog_admin.state_admin import PreModerateStates, AdminMainMenu, MarketingState, ListenAdmin


def start_admin_menu(**kwargs):
    return Window(
        Const('Admin mode'),
        Column(
            Button(text=Format('Менеджер постов'),
                   id='back_btn',
                   on_click=posts_manager_click),
            Button(text=Format('Яндекс погода'),
                   id='ya_weather_btn',
                   on_click=yandex_weather_click),
            Button(text=Format('Гости бота'),
                   id='guests_btn',
                   on_click=get_guests_click),
            Button(text=Format('Отправить рекламу'),
                   id='marketing_btn',
                   on_click=choose_marketing),
            WebApp(text=Const('Доброцен WebApp'), url=Const('https://1385988-ci25991.tw1.ru')),
            id='admin_main_id'
        ),
        state=AdminMainMenu.start
    )


def yandex_weather_window(**kwargs):
    return Window(
        Const("Жду скриншот"),
        MessageInput(callback_weather_handler, content_types=[ContentType.PHOTO]),
        state=ListenAdmin.get_weather_screen,
    )


def send_weather(**kwargs):
    return Window(
        DynamicMedia(selector='weather_photo'),
        Row(
            Button(Const("Отправить"), id="go_btn", on_click=send_weather_click),
            Button(Const("Отмена"), id="cancel_btn", on_click=weather_cancel)
        ),
        state=ListenAdmin.send_weather,
        getter=send_weather_photo
    )


def pre_moderate_posts_list(**kwargs):
    return Window(
        Const("Новые посты"),
        ScrollingGroup(
            Select(
                Format(text="{item.date} {item.source_title} {item.text}"),
                id='button',
                item_id_getter=attrgetter('internal_id'),
                items='posts_list_',
                on_click=select_post
            ),
            id='main',
            width=1,
            height=12,
            hide_on_single_page=True
        ),
        Button(Const("Очистить кэш"),
               id="clean_cash_btn",
               on_click=clean_cashe_folder),
        Button(Const(" -- Выход -- "),
               id="btn",
               on_click=dialog_close),
        state=PreModerateStates.post_list,
        getter=posts_list_getter
    )


def info_window(**kwargs):
    return Window(
        Multi(
            Format(text="Вложения: {attachments_info}", when=F['attachments_info']),
            Format("{date} {info.source} {info.source_title} "),
            Format("{text}"), when=F['text']),
        MediaScroll(
            DynamicMedia(selector='item'),
            id='media_scroll',
            items='files',
            when=F['files']
        ),
        NumberedPager(scroll='media_scroll', when=F['data']['files']),
        Url(Format("Ссылка на источник"),
            Format("{info.url}"), ),
        Url(Format("Автор {info.signer_name}"),
            Format("https://vk.com/id{info.signer_id}"), when=F['info.signer_id'] != 'Анонимно'),
        Button(text=Format('Опубликовать'),
               id='on_post_btn',
               on_click=on_go_post),
        Button(text=Format('<< Назад к списку постов'),
               id='back_button',
               on_click=start_list),
        Button(text=Format('Удалить'),
               id='delete_btn',
               on_click=on_delete),
        state=PreModerateStates.post_info,
        getter=post_info_getter
    )


def marketing_window(**kwargs):
    return Window(
        Const('Нужно выбрать'),
        Column(
            Button(Const("Реклама Доброцен"),
                   id="dobrotsen_btn",
                   on_click=send_dobrotsen),
            Button(Const("Реклама вакансий"),
                   id="leninowork_btn",
                   on_click=send_lenino_work)
        ),
        state=MarketingState.start
    )


def visitors(**kwargs):
    return Window(
        Format('{guests}'),
        Button(Const(" -- Выход -- "),
               id="btn",
               on_click=start_main_menu),
        state=AdminMainMenu.visitors,
        getter=get_guests_getter
    )
