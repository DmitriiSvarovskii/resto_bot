from aiogram.types import CallbackQuery

from src.lexicons import LEXICON_RU
from src.keyboards import product_keyboards, category_keyboards, main_keyboards
from src.utils import time_utils
from src.callbacks import CategoryIdCallbackFactory
from src.db import category_db, store_db, product_db


async def get_menu_category(callback: CallbackQuery):
    user_id = callback.message.chat.id

    if time_utils.is_valid_time_warning():
        await callback.answer(
            text=LEXICON_RU['closing_time_reminder'], show_alert=True)
        # await callback.message.edit_reply_markup(
        #     reply_markup=await main_keyboards.create_keyboard_main(user_id)
        # )

    store_info = await store_db.get_store_info()

    if store_info.is_active:
        categories = await category_db.get_all_categories()
        keyboard = await category_keyboards.create_keyboard_category(
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
            reply_markup=await main_keyboards.create_keyboard_main(user_id)
        )


async def get_menu_products(
    callback: CallbackQuery,
    callback_data: CategoryIdCallbackFactory
):
    products = await product_db.get_products_by_category(
        category_id=callback_data.category_id
    )

    keyboard = await product_keyboards.create_keyboard_product(
        products=products,
        user_id=callback.message.chat.id
    )

    if products:
        await callback.message.edit_text(text=LEXICON_RU['store'],
                                         reply_markup=keyboard)
    else:
        await callback.answer(text=LEXICON_RU['finish_category'],
                              show_alert=True)
