from aiogram.filters.state import State, StatesGroup


class FSMProductChangeCategory(StatesGroup):
    id = State()


class FSMProductChangeName(StatesGroup):
    name = State()


class FSMProductChangeDescription(StatesGroup):
    description = State()


class FSMProductChangePrice(StatesGroup):
    price = State()


class FSMProductChangePriceBox(StatesGroup):
    price_box = State()


class FSMProductDelete(StatesGroup):
    confirmation = State()
