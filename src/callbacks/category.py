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


class CategoryAdminAvailCallbackFactory(
    CategoryIdCallbackFactory,
    prefix="adm-av"
):
    pass
