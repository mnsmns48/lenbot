from aiogram.fsm.state import State, StatesGroup


class Vacancies(StatesGroup):
    vac_list = State()
    vac_info = State()
    finish = State()


class ListenUser(StatesGroup):
    to_admin_ = State()


class SuggestPost(StatesGroup):
    start = State()
    get_data = State()


class UserMainMenu(StatesGroup):
    start = State()


class SearchPhoneState(StatesGroup):
    start = State()
    get_phone_number = State()
