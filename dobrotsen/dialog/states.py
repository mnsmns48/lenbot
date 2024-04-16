from aiogram.fsm.state import StatesGroup, State


class DobrotsenMenu(StatesGroup):
    start = State()
    walking = State()
    products = State()