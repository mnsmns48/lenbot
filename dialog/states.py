from aiogram.fsm.state import State, StatesGroup


class Vacancies(StatesGroup):
    vac_list = State()
    second = State()

