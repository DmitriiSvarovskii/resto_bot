from aiogram.filters.callback_data import CallbackData
from .cart import CartEditCallbackFactory


class ProductIdCallbackFactory(
    CartEditCallbackFactory,
    prefix='pr',
):
    category_id: int


class ProductIdAdminCallbackFactory(
    ProductIdCallbackFactory,
    prefix='prad',
):
    pass


class AddProductAvailabilityCallbackFactory(
    CallbackData,
    prefix='prod-avail',
    sep='_'
):
    availability: bool
