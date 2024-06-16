from aiogram.fsm.state import StatesGroup, State


class AdminMainMenu(StatesGroup):
    start = State()
    visitors = State()


class PreModerateStates(StatesGroup):
    post_list = State()
    post_info = State()
    post_finish = State()


class MarketingState(StatesGroup):
    start = State()


class ListenAdmin(StatesGroup):
    get_weather_screen = State()
    send_weather = State()
