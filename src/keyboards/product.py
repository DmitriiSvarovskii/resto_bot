from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..lexicons import LEXICON_KEYBOARDS_RU
from ..callbacks import ProductIdCallbackFactory
from ..crud import read_cart_items_and_totals
from ..schemas import ReadProduct


async def create_keyboard_product(
    products: List[ReadProduct],
    user_id: int,
    session: AsyncSession,
):
    bill_data = await read_cart_items_and_totals(
        user_id=user_id,
        session=session
    )

    cart_items_dict = {
        item.product_id: item.quantity for item in bill_data.cart_items}

    keyboard = InlineKeyboardBuilder()

    for product in products:

        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductIdCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()))

        product_quantity = cart_items_dict.get(product.id, 0)

        keyboard.row(
            InlineKeyboardButton(
                text='Состав',
                callback_data=ProductIdCallbackFactory(
                    type_pr='compound',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()),
            InlineKeyboardButton(
                text=f'Цена: {product.price} ₹',
                callback_data='press_pass'
            ),
            InlineKeyboardButton(
                text=f'{product_quantity} шт',
                callback_data='press_pass'),
            width=3
        )

        keyboard.row(
            InlineKeyboardButton(
                text='➖',
                callback_data=ProductIdCallbackFactory(
                    type_pr='minus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()
            ),
            InlineKeyboardButton(
                text='➕',
                callback_data=ProductIdCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()
            ),
            width=2
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_menu'
        ),
        InlineKeyboardButton(
            text=f'Корзина 🛒 {bill_data.total_price} ₹',
            callback_data='press_cart'
        )
    )

    return keyboard.as_markup()
