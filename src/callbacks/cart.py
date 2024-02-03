from aiogram.filters.callback_data import CallbackData


class CartEditCallbackFactory(
    CallbackData,
    prefix='cart',
    sep='_'
):
    type_pr: str
    product_id: int
