from aiogram.filters.callback_data import CallbackData


class StoreCbData(
    CallbackData,
    prefix='store',
    sep='_'
):
    store_id: int
    type_update: str
