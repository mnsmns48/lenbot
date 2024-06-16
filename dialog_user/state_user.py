from aiogram.fsm.state import State, StatesGroup


class Vacancies(StatesGroup):
    vac_list = State()
    vac_info = State()
    finish = State()


class ListenUser(StatesGroup):
    suggest_ = State()
    to_public_ = State()
    to_admin_ = State()
    search_phone = State()


class UserMainMenu(StatesGroup):
    start = State()


class SearchPhoneState(StatesGroup):
    start = State()
    get_phone_number = State()

