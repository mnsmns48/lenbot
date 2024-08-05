from aiogram.fsm.state import State, StatesGroup


class Vacancies(StatesGroup):
    vac_list = State()
    vac_info = State()
    finish = State()


class ListenUser(StatesGroup):
    to_admin_ = State()
    suggest_ = State()


class UserMainMenu(StatesGroup):
    start = State()


class SearchPhoneState(StatesGroup):
    start = State()
    get_phone_number = State()


class Suggest(StatesGroup):
    suggest_choose = State()
    suggest_post = State()
    publish_post = State()
    suggest_work = State()

