import json
import os
from operator import attrgetter, itemgetter

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Column, Back, Url, NumberedPager
from aiogram_dialog.widgets.media import MediaScroll, DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi, ScrollingText, Text, List

from dialog_premoderate.callbacks_premode import dialog_close, select_post, start_list
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
    files_to_del = kwargs.get('files_to_del')
    if files_to_del:
        for file in kwargs.get('files_to_del'):
            os.remove(file)
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
        Button(text=Format('<< Назад к списку постов'),
               id='back_button',
               on_click=start_list),
        state=PreModerateStates.post_info,
        getter=post_info_getter
    )
