from aiogram.filters.callback_data import CallbackData


class CreateOrderCallbackFactory(
    CallbackData,
    prefix='order',
):
    order_type: int
    status: int
    mess_id: int


class CheckOrdersCallbackFactory(
    CreateOrderCallbackFactory,
    prefix='check',
    sep='_'
):
    order_id: int
    user_id: int


class TimeOrdersCallbackFactory(
    CheckOrdersCallbackFactory,
    prefix='time',
    sep='_'
):
    time: int


class OrderStatusCallbackFactory(
    CheckOrdersCallbackFactory,
    prefix='st',
    sep='_'
):
    pass
