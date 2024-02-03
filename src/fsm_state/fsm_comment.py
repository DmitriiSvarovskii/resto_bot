from aiogram.filters.state import State, StatesGroup


class FSMComment(StatesGroup):
    waiting_comment = State()
