from aiogram import Router, F, types

from src.lexicons import LEXICON_RU
from src.keyboards import category_kb, main_kb, product_kb
from src.utils import time_utils
from src.callbacks import CategoryIdCallbackFactory
from src.db import category_db, store_db, product_db


router = Router(name=__name__)


@router.callback_query(F.data == 'press_menu')
async def get_menu_category(callback: types.CallbackQuery):
    user_id = callback.message.chat.id

    if await time_utils.is_valid_time_warning():
        await callback.answer(
            text=LEXICON_RU['closing_time_reminder'], show_alert=True)

    store_info = await store_db.get_store_info()

    if store_info.is_active:
        categories = await category_db.get_all_categories()
        keyboard = await category_kb.create_kb_category(
            categories=categories,
            user_id=user_id,
        )

        await callback.message.edit_text(text=LEXICON_RU['category'],
                                         reply_markup=keyboard)
    else:
        await callback.answer(
            text=LEXICON_RU['store_not_active'],
            show_alert=True
        )
        await callback.message.edit_reply_markup(
            reply_markup=await main_kb.create_kb_main(user_id)
        )


@router.callback_query(CategoryIdCallbackFactory.filter())
async def get_menu_products(
    callback: types.CallbackQuery,
    callback_data: CategoryIdCallbackFactory
):
    products = await product_db.get_products_by_category(
        category_id=callback_data.category_id
    )

    keyboard = await product_kb.create_kb_product(
        products=products,
        user_id=callback.message.chat.id
    )

    if products:
        await callback.message.edit_text(text=LEXICON_RU['store'],
                                         reply_markup=keyboard)
    else:
        await callback.answer(text=LEXICON_RU['finish_category'],
                              show_alert=True)
