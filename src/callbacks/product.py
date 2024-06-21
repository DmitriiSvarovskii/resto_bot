from aiogram.filters.callback_data import CallbackData
from typing import Optional

from .cart import CartCallbackData


class ProductIdCallbackFactory(
    CartCallbackData,
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
    CartCallbackData,
    prefix='prod-chan-cat',
):
    pass


class ProductChangeNameCallbackFactory(
    CartCallbackData,
    prefix='prod-chan-nam',
):
    pass


class ProductChangeDescriptionCallbackFactory(
    CartCallbackData,
    prefix='prod-chan-des',
):
    pass


class ProductChangePriceCallbackFactory(
    CartCallbackData,
    prefix='prod-chan-pric',
):
    pass


class ProductChangePriceBoxCallbackFactory(
    CartCallbackData,
    prefix='prod-chan-pr-bx',
):
    pass


class ProductDeleteCallbackFactory(
    CartCallbackData,
    prefix='prod-del',
):
    pass
