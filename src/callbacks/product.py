from aiogram.filters.callback_data import CallbackData
from typing import Optional

from .cart import CartEditCallbackFactory


class ProductIdCallbackFactory(
    CartEditCallbackFactory,
    prefix='pr',
):
    popular: Optional[bool] = None
    category_id: int


class ProductIdAdminCallbackFactory(
    ProductIdCallbackFactory,
    prefix='prod',
):
    pass


class ProductChangeAdminCallbackFactory(
    ProductIdCallbackFactory,
    prefix='prod-ch',
):
    pass


class AddProductAvailabilityCallbackFactory(
    CallbackData,
    prefix='prod-avail',
    sep='_'
):
    availability: bool


class ProductChangeCategoryCallbackFactory(
    CartEditCallbackFactory,
    prefix='prod-chan-cat',
):
    pass


class ProductChangeNameCallbackFactory(
    CartEditCallbackFactory,
    prefix='prod-chan-nam',
):
    pass


class ProductChangeDescriptionCallbackFactory(
    CartEditCallbackFactory,
    prefix='prod-chan-des',
):
    pass


class ProductChangePriceCallbackFactory(
    CartEditCallbackFactory,
    prefix='prod-chan-pric',
):
    pass


class ProductChangePriceBoxCallbackFactory(
    CartEditCallbackFactory,
    prefix='prod-chan-pr-bx',
):
    pass


class ProductDeleteCallbackFactory(
    CartEditCallbackFactory,
    prefix='prod-del',
):
    pass
