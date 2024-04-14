from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Select, Column, Back
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog

from dobrotsen.dialog.callbacks import menu_selected
from dobrotsen.dialog.getters import menu_buttons
from dobrotsen.dialog.states import DobrotsenMenu

dialog = Dialog(
    Window(
        Const("Меню магазина Доброцен перед тобой"),
        Column(
            Select
            (Format(text="{item.title}"),
             id='button',
             item_id_getter=lambda item: item.id,
             items='menu',
             on_click=menu_selected
             ),
        ),

        getter=menu_buttons,
        state=DobrotsenMenu.main,
    ),

)
