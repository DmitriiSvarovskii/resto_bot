from aiogram.filters.state import State, StatesGroup


class FSMDeliveryAdmin(StatesGroup):
    waiting_name_rus = State()
    waiting_name_en = State()
    waiting_price = State()
    waiting_time = State()
