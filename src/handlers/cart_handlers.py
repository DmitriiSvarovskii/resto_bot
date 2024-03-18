from typing import Union
from aiogram import Router, F, types

from src.callbacks import ProductIdCallbackFactory, CartEditCallbackFactory
from src.lexicons import LEXICON_RU
from src.state import user_dict_comment
from src.keyboards import cart_kb, main_kb, product_kb
from src.db import product_db, cart_db
from src.utils import cart_utils


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
            popular=True
        )
    else:
        products = await product_db.get_products_by_category(
            category_id=callback_data.category_id
        )

        keyboard = await product_kb.create_kb_product(
            products=products,
            user_id=callback.message.chat.id
        )

    if callback_data.type_pr != 'compound':
        await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == 'press_cart')
async def press_cart(message: Union[types.CallbackQuery, types.Message]):

    user_id = message.message.chat.id if isinstance(
        message, types.CallbackQuery) else message.chat.id

    order_comment = cart_utils.get_comment_value(
        user_id=user_id,
        user_dict_comment=user_dict_comment
    )

    message_text, bill = await cart_utils.update_cart_message(
        user_id=user_id,
        order_comment=order_comment
    )

    reply_markup = cart_kb.create_kb_cart(
        mess_id=message.message.message_id if isinstance(
            message, types.CallbackQuery) else message.message_id
    )

    if bill:
        if isinstance(message, types.CallbackQuery):
            await message.message.edit_text(
                text=message_text,
                reply_markup=reply_markup
            )
        else:
            await message.answer(
                text=message_text,
                reply_markup=reply_markup
            )
    else:
        await message.answer(
            text=LEXICON_RU['empty_cart'],
            show_alert=True
        )


@router.callback_query(F.data == 'press_empty')
async def empty_cart(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    await cart_db.delete_cart_items_by_user_id(
        user_id=user_id,
    )
    await callback.message.edit_text(
        text=LEXICON_RU['empty_cart'],
        reply_markup=await main_kb.create_kb_main(user_id)
    )


@router.callback_query(F.data == 'press_edit_cart')
async def press_cart_edit(callback: types.CallbackQuery):
    await cart_kb.create_kbs_products_cart(
        callback=callback,
        user_id=callback.message.chat.id
    )


@router.callback_query(CartEditCallbackFactory.filter())
async def process_cart_edit(
    callback: types.CallbackQuery,
    callback_data: CartEditCallbackFactory
):
    await cart_utils.process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )

    await cart_kb.create_kbs_products_cart(
        callback=callback,
        user_id=callback.message.chat.id
    )
