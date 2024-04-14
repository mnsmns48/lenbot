from aiogram.fsm.state import StatesGroup, State


class DobrotsenMenu(StatesGroup):
    main = State()
    walking = State()
    product = State()