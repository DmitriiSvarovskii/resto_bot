from aiogram import Router, F, types

from src.callbacks import ProductIdCallbackFactory, CartCallbackData
from src.keyboards import cart_kb, main_kb, product_kb
from src.db import product_db, cart_db
from src.utils import cart_utils, redis_utils
from src.lexicons import text_cart_en, text_cart_ru


router = Router(name=__name__)


@router.callback_query(ProductIdCallbackFactory.filter())
async def adding_to_cart(
    callback: types.CallbackQuery,
    callback_data: ProductIdCallbackFactory,
):
    await cart_utils.process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )
    if callback_data.popular:
        products = await product_db.db_get_all_popular_products()

        keyboard = await product_kb.create_kb_product(
            products=products,
            user_id=callback.message.chat.id,
            popular=True,
            language=callback.from_user.language_code
        )
    else:
        products = await product_db.get_products_by_category(
            category_id=callback_data.category_id,
            store_id=callback_data.store_id
        )

        keyboard = await product_kb.create_kb_product(
            products=products,
            user_id=callback.message.chat.id,
            language=callback.from_user.language_code,
            store_id=callback_data.store_id
        )

    if callback_data.type_press != 'compound':
        await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(CartCallbackData.filter(F.type_press == "cart"))
async def press_cart(
    callback: types.CallbackQuery,
    callback_data: CartCallbackData
):
    if callback.from_user.language_code == 'ru':
        text_cart = text_cart_ru
    else:
        text_cart = text_cart_en

    user_id = callback.message.chat.id

    order_comment = await redis_utils.get_data_from_redis(
        key_prefix='order_comment',
        user_id=user_id,
    )
    if order_comment:
        order_comment = order_comment['order_comment']

    message_text, bill = await cart_utils.update_cart_message(
        store_id=callback_data.store_id,
        user_id=user_id,
        order_comment=order_comment,
        language=callback.from_user.language_code
    )

    reply_markup = cart_kb.create_kb_cart(
        store_id=callback_data.store_id,
        language=callback.from_user.language_code,
        mess_id=callback.message.message_id
    )

    if bill:
        await callback.message.edit_text(
            text=message_text,
            reply_markup=reply_markup
        )
    else:
        await callback.answer(
            text=text_cart.edit_cart_dict['empty_cart'],
            show_alert=True
        )


@router.callback_query(CartCallbackData.filter(F.type_press == 'empty-cart'))
async def empty_cart(
    callback: types.CallbackQuery,
    callback_data: CartCallbackData
):
    if callback.from_user.language_code == 'ru':
        text_cart = text_cart_ru
    else:
        text_cart = text_cart_en
    user_id = callback.message.chat.id
    await cart_db.delete_cart_items_by_user_id(
        user_id=user_id,
        store_id=callback_data.store_id
    )
    await callback.message.edit_text(
        text=text_cart.edit_cart_dict['empty_cart'],
        reply_markup=await main_kb.create_kb_main(
            language=callback.from_user.language_code,
            user_id=user_id,
            store_id=callback_data.store_id
        )
    )


@router.callback_query(CartCallbackData.filter(F.type_press == 'edit-cart'))
async def press_cart_edit(
    callback: types.CallbackQuery,
    callback_data: CartCallbackData
):
    if callback.from_user.language_code == 'ru':
        text_cart = text_cart_ru.edit_cart_dict
    else:
        text_cart = text_cart_en.edit_cart_dict

    keyboard = await cart_kb.create_kbs_products_cart(
        store_id=callback_data.store_id,
        user_id=callback.message.chat.id,
        language=callback.from_user.language_code
    )
    if keyboard:
        await callback.message.edit_text(
            text=text_cart['edit_cart'],
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text=text_cart['empty_cart'],
            reply_markup=await main_kb.create_kb_main(
                language=callback.from_user.language_code,
                user_id=callback.message.chat.id,
                store_id=callback_data.store_id
            )
        )


@router.callback_query(CartCallbackData.filter())
async def process_cart_edit(
    callback: types.CallbackQuery,
    callback_data: CartCallbackData
):
    if callback.from_user.language_code == 'ru':
        text_cart = text_cart_ru.edit_cart_dict
    else:
        text_cart = text_cart_en.edit_cart_dict
    await cart_utils.process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )

    keyboard = await cart_kb.create_kbs_products_cart(
        store_id=callback_data.store_id,
        user_id=callback.message.chat.id,
        language=callback.from_user.language_code
    )
    if keyboard:
        await callback.message.edit_text(
            text=text_cart['edit_cart'],
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text=text_cart['empty_cart'],
            reply_markup=await main_kb.create_kb_main(
                language=callback.from_user.language_code,
                user_id=callback.message.chat.id,
                store_id=callback_data.store_id
            )
        )
