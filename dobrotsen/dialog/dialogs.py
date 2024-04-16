from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Select, Column, Back, ScrollingGroup, Multiselect
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog

from dobrotsen.dialog.callbacks import menu_selected
from dobrotsen.dialog.getters import main_menu, walking_menu, show_products
from dobrotsen.dialog.states import DobrotsenMenu

# dialog = Dialog(
#     Window(
#         Format(text="{catalog}:\n"),
#         ScrollingGroup(
#             Select
#             (Format(text="{item.title}"),
#              id='button',
#              item_id_getter=attrgetter('id'),
#              items='menu',
#              type_factory=int,
#              on_click=menu_selected
#              ),
#             id='main',
#             width=1,
#             height=6
#         ),
#         getter=main_menu,
#         state=DobrotsenMenu.main,
#     ),
# )
dialog = Dialog(
    Window(
        Const(text="Главное меню:\n"),
        ScrollingGroup(
            Select
            (Format(text="{item.title}"),
             id='button',
             item_id_getter=attrgetter('id'),
             items='menu',
             type_factory=int,
             on_click=menu_selected
             ),
            id='main',
            width=1,
            height=9
        ),
        getter=main_menu,
        state=DobrotsenMenu.start,
    ),
    Window(
        Format(text="{catalog}:\n"),
        Column(
            Select
            (Format(text="{item.title}"),
             id='button',
             item_id_getter=attrgetter('id'),
             items='menu',
             type_factory=int,
             on_click=menu_selected
             ),
            # id='main',
            # width=1,
            # height=7
        ),
        Back(Const('<<<  Предыдущее меню')),
        getter=walking_menu,
        state=DobrotsenMenu.walking,
    ),
    Window(
        Format(text="{catalog}:\n"),
        Column(
            Select
            (Format(text="{item.price} {item.title}"),
             id='button',
             item_id_getter=attrgetter('id'),
             items='menu',
             type_factory=int,
             on_click=menu_selected
             ),
            id='main',
            # width=1,
            # height=7
        ),
        Back(Const('<<<  назад')),
        getter=show_products,
        state=DobrotsenMenu.products,
    ),
)
