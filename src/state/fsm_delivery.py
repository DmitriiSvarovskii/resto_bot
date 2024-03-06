from aiogram.filters.state import State, StatesGroup


class FSMDeliveryInfo(StatesGroup):
    waiting_delivery_id = State()
    waiting_number_phone = State()
    waiting_guide = State()
    waiting_location = State()
