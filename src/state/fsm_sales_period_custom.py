from aiogram.filters.state import State, StatesGroup


class FSMSalesPeriodCustom(StatesGroup):
    start_date = State()
    end_date = State()
