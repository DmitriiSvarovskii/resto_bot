from aiogram.types import CallbackQuery
from typing import Optional

from src.lexicons import LEXICON_RU,  text_cart_en, text_cart_ru
from src.callbacks import ProductIdCallbackFactory
from src.db import cart_db
from src.schemas import cart_schemas


async def process_cart_action(
    callback: CallbackQuery,
    callback_data: ProductIdCallbackFactory,
):
    product_id = callback_data.product_id
    user_id = callback.message.chat.id

    cart_data = cart_schemas.CartCreate(
        product_id=product_id,
        user_id=user_id,
        store_id=callback_data.store_id,
    )

    type_press = callback_data.type_press

    if type_press == 'plus':
        response = await cart_db.add_to_cart(
            data=cart_data,
        )
        await callback.answer(text=response['message'])

    elif type_press == 'minus':
        response = await cart_db.decrease_cart_item(
            data=cart_data,
        )
        if response['message'] == LEXICON_RU['cart_error']:
            await callback.answer(
                text=response['message'],
                show_alert=True
            )
        await callback.answer(text=response['message'])

    elif type_press == 'compound':
        compound_text = await cart_db.get_one_product(
            product_id=cart_data.product_id,
            store_id=cart_data.store_id
        )
        description = (compound_text.description_rus
                       if callback.from_user.language_code == 'ru'
                       else compound_text.description_en)

        await callback.answer(
            text=description,
            show_alert=True
        )

    elif type_press == 'del':
        await cart_db.delete_cart_item(
            data=cart_data,
        )
        await callback.answer(text='message')


async def update_cart_message(
    user_id: int,
    language: str,
    store_id: int,
    order_comment: Optional[str] = None
) -> None:
    if language == 'ru':
        text_cart = text_cart_ru
    else:
        text_cart = text_cart_en

    response = await cart_db.get_cart_items_and_totals(
        user_id=user_id,
        store_id=store_id
    )

    bill = response.total_price
    order_text = ''
    box_price = 0

    for item in response.cart_items:
        category_name = item.category_name_rus if language == 'ru' else item.category_name_en
        product_name = item.name_rus if language == 'ru' else item.name_en
        order_text += (
            f'{category_name} - '
            f'{product_name} x '
            f'{item.quantity} - '
            f'{item.unit_price} ₹\n\n'
        )
        if item.box_price:
            box_price += item.box_price

    message_text = text_cart.create_cart_text(
        bill=bill,
        order_text=order_text,
        order_comment=order_comment,
        box_price=box_price,
    )

    return message_text, bill
