from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional, List

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.schemas import GetCategory
from src.callbacks import (
    CategoryIdCallbackFactory,
)
from src.crud import read_cart_items_and_totals


async def create_keyboard_category(
    categories: List[GetCategory],
    user_id: int,
    session,
):
    bill_data = await read_cart_items_and_totals(
        user_id=user_id,
        session=session
    )

    keyboard = InlineKeyboardBuilder()

    row_buttons = []

    for category in categories:

        button = InlineKeyboardButton(
            text=f'{category.name}',
            callback_data=CategoryIdCallbackFactory(
                category_id=category.id).pack()
        )
        row_buttons.append(button)

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    keyboard.row(*row_buttons, width=2)
    bill = 0
    if bill_data.total_price:
        bill = bill_data.total_price

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_main_menu'
        ),
        InlineKeyboardButton(
            text=f'Корзина 🛒 {bill} ₹',
            callback_data='press_cart'
        )
    )

    return keyboard.as_markup()
