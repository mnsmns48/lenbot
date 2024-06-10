from aiogram.fsm.state import StatesGroup, State


class PreModerateStates(StatesGroup):
    post_list = State()
    post_info = State()
    post_finish = State()
