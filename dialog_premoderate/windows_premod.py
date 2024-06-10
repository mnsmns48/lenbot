from operator import attrgetter, itemgetter
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Column, Back
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialog_premoderate.callbacks_premode import dialog_close, select_post
from dialog_premoderate.getters_premode import posts_list_getter, post_info_getter
from dialog_premoderate.states_premod import PreModerateStates


def pre_moderate_posts(**kwargs):
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
            height=10,
            hide_on_single_page=True
        ),
        Button(Const(" -- Выход -- "),
               id="btn",
               on_click=dialog_close),
        state=PreModerateStates.post_list,
        getter=posts_list_getter
    )


def info_window(**kwargs):
    return Window(
        Multi(
            Format("Дата: {info.date}"),
            Format("{info.text}")),

        Column(Back(Const("<< Назад к списку постов"))),
        state=PreModerateStates.post_info,
        getter=post_info_getter
    )
