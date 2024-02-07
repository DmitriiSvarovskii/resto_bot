from typing import Union
from aiogram.types import CallbackQuery, Message

from src.callbacks import ProductIdCallbackFactory, CartEditCallbackFactory
from src.lexicons import LEXICON_RU
from src.fsm_state import user_dict_comment
from src.keyboards import (
    create_keyboards_products_cart, create_keyboard_cart
)
from src.keyboards import product_keyboards, main_keyboards
from src.db import product_db, cart_db
from src.utils_new import cart_utils


async def adding_to_cart(
    callback: CallbackQuery,
    callback_data: ProductIdCallbackFactory,
):

    await cart_utils.process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )

    products = await product_db.get_products_by_category(
        category_id=callback_data.category_id
    )

    keyboard = await product_keyboards.create_keyboard_product(
        products=products,
        user_id=callback.message.chat.id
    )
    await callback.message.edit_reply_markup(reply_markup=keyboard)


async def press_cart(message: Union[CallbackQuery, Message]):
    if isinstance(message, CallbackQuery):
        user_id = message.message.chat.id
    else:
        user_id = message.chat.id

    comment_value = cart_utils.get_comment_value(
        user_id=user_id,
        user_dict_comment=user_dict_comment
    )

    message_text, bill = await cart_utils.update_cart_message(
        user_id=user_id,
        message=message,
        comment=comment_value
    )

    if bill:
        if isinstance(message, CallbackQuery):
            await message.message.edit_text(
                text=message_text,
                reply_markup=create_keyboard_cart(
                    mess_id=message.message.message_id
                )
            )
        else:
            await message.answer(
                text=message_text,
                reply_markup=create_keyboard_cart(
                    mess_id=message.message_id
                )
            )
    else:
        if isinstance(message, CallbackQuery):
            await message.answer(
                text=LEXICON_RU['empty_cart'],
                show_alert=True
            )
        else:
            await message.answer(
                text=LEXICON_RU['empty_cart'],
                show_alert=True
            )


async def empty_cart(callback: CallbackQuery):
    user_id = callback.message.chat.id
    await cart_db.delete_cart_items_by_user_id(
        user_id=user_id,
    )
    await callback.message.edit_text(
        text=LEXICON_RU['empty_cart'],
        reply_markup=await main_keyboards.create_keyboard_main(user_id)
    )


async def press_cart_edit(callback: CallbackQuery):
    await create_keyboards_products_cart(
        callback=callback,
        user_id=callback.message.chat.id
    )


async def process_cart_edit(
    callback: CallbackQuery,
    callback_data: CartEditCallbackFactory
):
    await cart_utils.process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )

    await create_keyboards_products_cart(
        callback=callback,
        user_id=callback.message.chat.id
    )
