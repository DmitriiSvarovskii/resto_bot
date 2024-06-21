from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CartCallbackData(
    CallbackData,
    prefix='cart',
    sep='_'
):
    type_press: Optional[str] = None
    store_id: Optional[int] = None
    product_id: Optional[int] = None
