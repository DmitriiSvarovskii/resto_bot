from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import category_kb, product_kb
from src.db import product_db, category_db
from src.callbacks import (
    CategoryAdminChangeCallbackFactory,
    ProductChangeAdminCallbackFactory,
    StoreAdminCbData
)


router = Router(name=__name__)


@router.callback_query(
    StoreAdminCbData.filter(F.type_press == 'change-product')
)
async def process_change_product(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    categories = await category_db.get_all_categories(
        store_id=callback_data.store_id
    )
    keyboard = await category_kb.create_kb_category_admin(
        store_id=callback_data.store_id,
        categories=categories,
        callback_data=CategoryAdminChangeCallbackFactory,
        language=callback.from_user.language_code
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
        category_id=callback_data.category_id,
        store_id=callback_data.store_id
    )

    keyboard = await product_kb.create_kb_change_product_list(
        products=products,
        language=callback.from_user.language_code,
        store_id=callback_data.store_id
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
            category_id=callback_data.category_id,
            store_id=callback_data.store_id
        )
        await callback.message.edit_text(text='Выберите необходимый пункт',
                                         reply_markup=keyboard)
        await callback.answer(text='Ок')
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )
