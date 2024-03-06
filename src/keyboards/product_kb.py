from typing import List
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.callbacks import (
    ProductIdCallbackFactory,
    ProductIdAdminCallbackFactory
)
from src.schemas import product_schemas
from src.db import cart_db


async def create_kb_product(
    products: List[product_schemas.ReadProduct],
    user_id: int,
):
    cart_info = await cart_db.get_cart_items_and_totals(
        user_id=user_id
    )

    cart_items_dict = {
        item.product_id: item.quantity for item in cart_info.cart_items}

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
            text=f'Корзина 🛒 {cart_info.total_price} ₹',
            callback_data='press_cart'
        )
    )

    return keyboard.as_markup()


async def create_kb_product_admin(
    products: List[product_schemas.ReadProduct],
):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        availability = "В наличии" if product.availability else "Отсутствует"
        indicator = '✅' if product.availability else '❌'
        action = "Убрать" if product.availability else "Добавить"

        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()),
            InlineKeyboardButton(
                text=indicator,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()),
            width=3
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_modify_avail_prod'
        )
    )

    return keyboard.as_markup()
