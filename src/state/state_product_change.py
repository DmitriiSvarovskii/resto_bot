from aiogram.filters.state import State, StatesGroup


class FSMProductChangeCategory(StatesGroup):
    id = State()


class FSMProductChangeName(StatesGroup):
    name_rus = State()
    name_en = State()


class FSMProductChangeDescription(StatesGroup):
    description_rus = State()
    description_en = State()


class FSMProductChangePrice(StatesGroup):
    price = State()


class FSMProductChangePriceBox(StatesGroup):
    price_box = State()


class FSMProductDelete(StatesGroup):
    confirmation = State()
