from aiogram.filters.state import State, StatesGroup


class FSMCategoryChangeName(StatesGroup):
    name_rus = State()
    name_en = State()


class FSMCategoryDelete(StatesGroup):
    confirmation = State()
