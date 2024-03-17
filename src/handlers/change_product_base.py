from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import category_kb, product_kb
from src.db import product_db, category_db
from src.callbacks import (
    CategoryAdminChangeCallbackFactory,
    ProductChangeAdminCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_change_product')
async def process_change_product(callback: types.CallbackQuery):
    categories = await category_db.get_all_categories()
    keyboard = await category_kb.create_kb_category_admin(
        categories=categories,
        callback_data=CategoryAdminChangeCallbackFactory
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


@router.callback_query(CategoryAdminChangeCallbackFactory.filter())
async def get_admin_products(
    callback: types.CallbackQuery,
    callback_data: CategoryAdminChangeCallbackFactory
):
    products = await product_db.get_products_by_category_admin(
        category_id=callback_data.category_id
    )

    keyboard = await product_kb.create_kb_change_product_list(
        products=products
    )

    await callback.message.edit_text(text='Продукты',
                                     reply_markup=keyboard)
    await callback.answer(text='Ок')


@router.callback_query(ProductChangeAdminCallbackFactory.filter())
async def get_admin_change_avail_products(
    callback: types.CallbackQuery,
    callback_data: ProductChangeAdminCallbackFactory
):
    try:
        keyboard = await product_kb.create_kb_change_product(
            product_id=callback_data.product_id,
            category_id=callback_data.category_id
        )
        await callback.message.edit_text(text='Выберите необходимый пункт',
                                         reply_markup=keyboard)
        await callback.answer(text='Ок')
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )
