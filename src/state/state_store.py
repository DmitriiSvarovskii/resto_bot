from aiogram.filters.state import State, StatesGroup


class FSMStore(StatesGroup):
    waiting_location = State()
    waiting_welcome_text = State()
    waiting_manager_group = State()
    waiting_sale_group = State()
