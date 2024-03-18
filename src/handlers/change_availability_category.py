from aiogram import types, Router, F

from src.keyboards import category_kb
from src.db import category_db
from src.callbacks import (
    CategoryAdminCallbackFactory,
    CategoryAdminAvailCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_modify_avail_categ')
async def process_modify_availability_categories(
    callback: types.CallbackQuery
):
    categories = await category_db.get_all_categories_admin()
    keyboard = await category_kb.create_kb_category_avail_admin(
        categories=categories
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
    print(2)
    await category_db.change_avail_category(callback_data.category_id)
    categories = await category_db.get_all_categories_admin()
    keyboard = await category_kb.create_kb_category_avail_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )
