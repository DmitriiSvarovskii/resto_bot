from aiogram.filters.state import State, StatesGroup


class FSMAddNewCategory(StatesGroup):
    category_name = State()
    availability = State()
    check = State()
