from aiogram.fsm.state import StatesGroup, State


class ListenUser(StatesGroup):
    suggest_ = State()
    to_public_ = State()
    to_admin_ = State()
    search_phone = State()


class ListenAdmin(StatesGroup):
    get_weather_screen = State()
    send_weather = State()
