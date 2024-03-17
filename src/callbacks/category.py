from aiogram.filters.callback_data import CallbackData


class CategoryIdCallbackFactory(
    CallbackData,
    prefix="ctg"
):
    category_id: int


class CategoryAdminCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm"
):
    pass


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
    category_name: str


class AddCategoryAvailabilityCallbackFactory(
    CallbackData,
    prefix='cat-avail',
    sep='_'
):
    availability: bool
