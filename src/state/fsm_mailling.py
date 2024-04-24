from aiogram.filters.state import State, StatesGroup


class FSMMailingPhoto(StatesGroup):
    waiting_photo = State()
    waiting_text = State()
    waiting_check = State()
