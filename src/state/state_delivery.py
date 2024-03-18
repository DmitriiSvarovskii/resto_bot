from aiogram.filters.state import State, StatesGroup


class FSMDeliveryAdmin(StatesGroup):
    waiting_name = State()
    waiting_price = State()
    waiting_time = State()
