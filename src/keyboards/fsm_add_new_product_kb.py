from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
)

from src.schemas import category_schemas
from src.lexicons import LEXICON_KEYBOARDS_RU
from src.callbacks import (
    AddProductAvailabilityCallbackFactory,
    CategoryAdminAddCallbackFactory,
)


def create_kb_approval():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='press_approval_prod')
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Внести изменения',
            callback_data='press_make_changes_prod')
    )

    return keyboard.as_markup()


def create_kb_availability():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='В наличии',
            callback_data=AddProductAvailabilityCallbackFactory(
                availability=True
            ).pack()
        ),
        InlineKeyboardButton(
            text='Отсутствует',
            callback_data=AddProductAvailabilityCallbackFactory(
                availability=False
            ).pack()
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


def create_kb_fsm_canel() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel_add_product'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


def create_kb_fsm_canel_and_skip() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel_add_product'])
    button_2 = KeyboardButton(text=LEXICON_KEYBOARDS_RU['skip'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2]],
        resize_keyboard=True
    )
    return keyboard
