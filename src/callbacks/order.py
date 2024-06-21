from aiogram.filters.callback_data import CallbackData
from typing import Optional


class OrderCallbackFactory(
    CallbackData,
    prefix='order',
):
    type_callback: Optional[str] = None
    order_type: Optional[int] = None
    status: int
    mess_id: Optional[int] = None
    language: str
    store_id: int


class CreateOrderCallbackFactory(
    CallbackData,
    prefix='order',
):
    type_callback: Optional[str] = None
    order_type: Optional[int] = None
    status: int
    store_id: int
    mess_id: Optional[int] = None
    language: str


class CheckOrdersCallbackFactory(
    CreateOrderCallbackFactory,
    prefix='check',
    sep='_'
):
    order_id: int
    user_id: int


class AccountOrdersCbData(
    CallbackData,
    prefix='account',
    sep='_'
):
    type_callback: Optional[str] = None
    order_id: int
    user_id: int


class TimeOrdersCallbackFactory(
    CheckOrdersCallbackFactory,
    prefix='time',
    sep='_'
):
    time: int
    time_del: Optional[int] = None


class OrderStatusCallbackFactory(
    CheckOrdersCallbackFactory,
    prefix='st',
    sep='_'
):
    pass
