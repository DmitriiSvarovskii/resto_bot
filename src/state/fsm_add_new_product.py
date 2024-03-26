from aiogram.filters.state import State, StatesGroup


class FSMAddNewProduct(StatesGroup):
    category_id = State()
    product_name_rus = State()
    product_name_en = State()
    description_rus = State()
    description_en = State()
    price = State()
    price_box = State()
    availability = State()
    check = State()
