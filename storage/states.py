from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    age_question = State()
    sex_question = State()
    location_share = State()
    location_write = State()
