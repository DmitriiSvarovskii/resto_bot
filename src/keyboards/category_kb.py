from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from typing import List, Optional

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.schemas import category_schemas
from src.callbacks import (
    CategoryIdCallbackFactory,
    CategoryChangeNameCallbackFactory,
    CategoryDeleteCallbackFactory,
    CategoryAdminAvailCallbackFactory,
    CategoryAdminAddCallbackFactory,
)
from src.db import cart_db


async def create_kb_category(
    categories: List[category_schemas.GetCategory],
    user_id: int,
):
    bill = await cart_db.get_total_price_cart(
        user_id=user_id
    )

    keyboard = InlineKeyboardBuilder()

    row_buttons = []

    row_buttons.append(
        InlineKeyboardButton(
            text='Популярное 🔥',
            callback_data='press_popular_menu'
        ),
    )

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


async def create_kb_category_admin(
    categories: List[category_schemas.GetCategory],
    callback_data: CallbackData,
    popular: Optional[bool] = None
):

    keyboard = InlineKeyboardBuilder()

    row_buttons = [
        InlineKeyboardButton(
            text=f'{category.name}',
            callback_data=callback_data(
                category_id=category.id, popular=popular).pack()
        )
        for category in categories
    ]

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    keyboard.row(*row_buttons, width=2)

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_edit_menu'
        )
    )

    return keyboard.as_markup()


async def create_kb_category_admin_add_prod(
    categories: List[category_schemas.GetCategory],
):

    keyboard = InlineKeyboardBuilder()

    row_buttons = [
        InlineKeyboardButton(
            text=f'{category.name}',
            callback_data=CategoryAdminAddCallbackFactory(
                category_id=category.id,
                category_name=category.name
            ).pack()
        )
        for category in categories
    ]

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    keyboard.row(*row_buttons, width=2)

    return keyboard.as_markup()


async def create_kb_category_avail_admin(
    categories: List[category_schemas.GetCategory],
):

    keyboard = InlineKeyboardBuilder()

    for category in categories:
        availability = "В наличии" if category.availability else "Отсутствует"
        indicator = '✅' if category.availability else '❌'
        action = "Убрать" if category.availability else "Добавить"

        keyboard.row(
            InlineKeyboardButton(
                text=f'{category.name}',
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ),
            InlineKeyboardButton(
                text=indicator,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ),
            width=3
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_edit_menu'
        )
    )

    return keyboard.as_markup()


async def create_kb_change_category(
    category_id: int,
):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text='Изменить название категории ✏️',
            callback_data=CategoryChangeNameCallbackFactory(
                category_id=category_id
            ).pack()),
        InlineKeyboardButton(
            text='Удалить товар ✖',
            callback_data=CategoryDeleteCallbackFactory(
                category_id=category_id
            ).pack()),
        width=1
    )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_admin'
        )
    )

    return keyboard.as_markup()


def create_kb_fsm_change_name() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отменить изменение')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


async def create_kb_category_delete():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='press_approval_delete_category'
        ),
        InlineKeyboardButton(
            text='Отменить',
            callback_data='press_cancel_delete_category'
        ),
        width=2
    )

    return keyboard.as_markup()
