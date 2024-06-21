from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CategoryIdCallbackFactory(
    CallbackData,
    prefix="ctg"
):
    category_id: int
    store_id: int


class CategoryAdminCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm"
):
    popular: Optional[bool] = None


class CategoryAdminChangeCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm-ch"
):
    pass


class CategoryChangeCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="cat-chan"
):
    pass


class ChangeCategoryProductCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="chan-prod-cat"
):
    pass


class CategoryAdminAvailCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm-av"
):
    pass


class CategoryChangeNameCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm-chan-name"
):
    pass


class CategoryDeleteCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm-del"
):
    pass


class CategoryAdminAddCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm-add"
):
    pass


class AddCategoryAvailabilityCallbackFactory(
    CallbackData,
    prefix='cat-avail',
    sep='_'
):
    availability: bool
