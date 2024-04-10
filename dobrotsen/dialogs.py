from aiogram.filters.state import StatesGroup, State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog


class MySG(StatesGroup):
    dialog = State()


main_window = Window(
    Const("Hello, its dialog"),  # just a constant text
    Button(Const("Useless button"), id="nothing"),  # button with text and id
    state=MySG.dialog,  # state is used to identify window between dialogs
)

dialog = Dialog(main_window)
