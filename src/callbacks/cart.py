from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CartEditCallbackFactory(
    CallbackData,
    prefix='cart',
    sep='_'
):
    type_pr: Optional[str] = None
    product_id: int
