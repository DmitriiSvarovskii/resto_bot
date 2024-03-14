from aiogram.filters.state import State, StatesGroup


class FSMAddNewProduct(StatesGroup):
    category_id = State()
    product_name = State()
    description = State()
    price = State()
    price_box = State()
    availability = State()
    check = State()
