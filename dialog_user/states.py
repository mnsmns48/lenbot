from aiogram.fsm.state import State, StatesGroup


class Vacancies(StatesGroup):
    vac_list = State()
    vac_info = State()
    finish = State()