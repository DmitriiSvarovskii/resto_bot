from aiogram.types import CallbackQuery

from src.database import get_async_session
from src.crud import delete_cart_items_by_user_id
from src.callbacks import ProductIdCallbackFactory, CartEditCallbackFactory
from src.lexicons import LEXICON_RU
from src.utils import update_cart_message, get_comment_value
from src.fsm_state import user_dict_comment
from src.keyboards import (
    create_keyboard_product,
    create_keyboard_main,
    create_keyboards_products_cart,
)
from .utils import get_products_by_category, process_cart_action


async def adding_to_cart(
    callback: CallbackQuery,
    callback_data: ProductIdCallbackFactory,
):

    await process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )

    async for session in get_async_session():
        products = await get_products_by_category(
            category_id=callback_data.category_id,
        )

        keyboard = await create_keyboard_product(
            products=products,
            user_id=callback.message.chat.id,
            session=session
        )
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        break


async def press_cart(callback: CallbackQuery):
    user_id = callback.message.chat.id

    comment_value = get_comment_value(
        user_id=user_id,
        user_dict_comment=user_dict_comment
    )

    await update_cart_message(
        user_id=user_id,
        message=callback,
        comment=comment_value
    )


async def empty_cart(callback: CallbackQuery):
    async for session in get_async_session():
        await delete_cart_items_by_user_id(
            user_id=callback.message.chat.id,
            session=session
        )
        break
    await callback.message.edit_text(
        text=LEXICON_RU['empty_cart'],
        reply_markup=await create_keyboard_main(callback.message.chat.id)
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
    await process_cart_action(
        callback=callback,
        callback_data=callback_data,
    )

    await create_keyboards_products_cart(
        callback=callback,
        user_id=callback.message.chat.id
    )
