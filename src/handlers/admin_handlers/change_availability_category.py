from aiogram import types, Router, F

from src.keyboards import category_kb
from src.db import category_db
from src.callbacks import (
    CategoryAdminCallbackFactory,
    CategoryAdminAvailCallbackFactory,
    StoreAdminCbData
)


router = Router(name=__name__)


@router.callback_query(StoreAdminCbData.filter(
    F.type_press == 'modify-avail-categ')
)
async def process_modify_availability_categories(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    categories = await category_db.get_all_categories_admin(
        store_id=callback_data.store_id
    )
    keyboard = await category_kb.create_kb_category_avail_admin(
        categories=categories,
        language=callback.from_user.language_code,
        store_id=callback_data.store_id
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


@router.callback_query(CategoryAdminAvailCallbackFactory.filter())
async def process_press_availability_categories(
    callback: types.CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    await category_db.change_avail_category(
        category_id=callback_data.category_id,
        store_id=callback_data.store_id
    )
    categories = await category_db.get_all_categories_admin(
        store_id=callback_data.store_id
    )
    keyboard = await category_kb.create_kb_category_avail_admin(
        categories=categories,
        language=callback.from_user.language_code,
        store_id=callback_data.store_id
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )
