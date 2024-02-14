from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.db import customer_db


async def create_keyboard_main(user_id: Optional[int] = None):
    user_info = await customer_db.get_user_info_by_id(
        user_id=user_id
    )
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['menu'],
            callback_data='press_menu'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['contact'],
            callback_data='press_contact'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['delivery'],
            callback_data='press_delivery'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['location'],
            callback_data='press_location'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['personal_account'],
            callback_data='press_account'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['group_telegram'],
            url='https://t.me/PizzaGoaFood'),
    ]
    button_admin = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['admin'],
        callback_data='press_admin')

    keyboard = InlineKeyboardBuilder()

    keyboard.row(*buttons, width=2)

    if user_info.admin:
        keyboard.row(button_admin, width=1)

    return keyboard.as_markup()
