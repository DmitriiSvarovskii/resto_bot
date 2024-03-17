from aiogram.filters.state import State, StatesGroup


class FSMOpeningHours(StatesGroup):
    opening_time = State()
    closing_time = State()
