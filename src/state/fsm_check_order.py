from aiogram.filters.state import State, StatesGroup


class FSMCheckOrder(StatesGroup):
    order_id = State()
