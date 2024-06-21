from aiogram.filters.callback_data import CallbackData

from typing import Optional


class StoreCbData(
    CallbackData,
    prefix='store',
    sep='_'
):
    store_id: int
    type_update: str


class StoreCbDataList(
    CallbackData,
    prefix='store',
    sep='_'
):
    store_id: int
    type_press: Optional[str] = None


class StoreMenuCbData(
    StoreCbDataList,
    prefix='store-menu',
    sep='_'
):
    type: str


class StoreAdminCbData(
    StoreCbDataList,
    prefix='store-admin',
    sep='_'
):
    pass
