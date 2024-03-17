from aiogram.filters.state import State, StatesGroup


class FSMCategoryChangeName(StatesGroup):
    name = State()


class FSMCategoryDelete(StatesGroup):
    confirmation = State()
