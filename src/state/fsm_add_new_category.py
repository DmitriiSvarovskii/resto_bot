from aiogram.filters.state import State, StatesGroup


class FSMAddNewCategory(StatesGroup):
    category_name_rus = State()
    category_name_en = State()
    availability = State()
    check = State()
