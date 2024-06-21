from aiogram import Router, F, types

from src.utils import time_utils
from src.callbacks import CategoryIdCallbackFactory, StoreMenuCbData
from src.lexicons import text_menu_en, text_menu_ru
from src.db import category_db, store_db, product_db
from src.keyboards import category_kb, main_kb, product_kb


router = Router(name=__name__)


@router.callback_query(StoreMenuCbData.filter(F.type == 'menu'))
async def get_menu_category(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    user_id = callback.message.chat.id

    if callback.from_user.language_code == 'ru':
        text_menu = text_menu_ru
    else:
        text_menu = text_menu_en

    if await time_utils.is_valid_time_warning(store_id=callback_data.store_id):
        await callback.answer(
            text=text_menu.menu_messages_dict['closing_time_reminder'],
            show_alert=True
        )

    store_info = await store_db.get_store_info(store_id=callback_data.store_id)

    if store_info.is_active:
        categories = await category_db.get_all_categories(
            store_id=callback_data.store_id
        )
        keyboard = await category_kb.create_kb_category(
            store_id=callback_data.store_id,
            categories=categories,
            user_id=user_id,
            language=callback.from_user.language_code
        )

        await callback.message.edit_text(
            text=text_menu.menu_messages_dict['category'],
            reply_markup=keyboard
        )
    else:
        await callback.answer(
            text=text_menu.menu_messages_dict['store_not_active'],
            show_alert=True
        )
        await callback.message.edit_reply_markup(
            reply_markup=await main_kb.create_kb_main(
                language=callback.from_user.language_code,
                user_id=user_id
            )
        )


@router.callback_query(CategoryIdCallbackFactory.filter())
async def get_menu_products(
    callback: types.CallbackQuery,
    callback_data: CategoryIdCallbackFactory
):
    if callback.from_user.language_code == 'ru':
        text_menu = text_menu_ru
    else:
        text_menu = text_menu_en

    products = await product_db.get_products_by_category(
        store_id=callback_data.store_id,
        category_id=callback_data.category_id
    )

    keyboard = await product_kb.create_kb_product(
        products=products,
        user_id=callback.message.chat.id,
        language=callback.from_user.language_code,
        store_id=callback_data.store_id
    )

    if products:
        await callback.message.edit_text(
            text=text_menu.menu_messages_dict['product'],
            reply_markup=keyboard
        )
    else:
        await callback.answer(
            text=text_menu.menu_messages_dict['finish_category'],
            show_alert=True
        )


@router.callback_query(StoreMenuCbData.filter(F.type == 'popular'))
async def get_menu_products_popular(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    if callback.from_user.language_code == 'ru':
        text_menu = text_menu_ru
    else:
        text_menu = text_menu_en

    products = await product_db.db_get_all_popular_products(
        store_id=callback_data.store_id
    )

    keyboard = await product_kb.create_kb_product(
        products=products,
        store_id=callback_data.store_id,
        user_id=callback.message.chat.id,
        popular=True,
        language=callback.from_user.language_code
    )

    if products:
        await callback.message.edit_text(
            text=text_menu.menu_messages_dict['product'],
            reply_markup=keyboard
        )
    else:
        await callback.answer(
            text=text_menu.menu_messages_dict['finish_category'],
            show_alert=True
        )
