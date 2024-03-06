from aiogram.filters.state import State, StatesGroup


class FSMQrCode(StatesGroup):
    waiting_link = State()
