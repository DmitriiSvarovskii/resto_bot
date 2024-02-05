from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..lexicons import LEXICON_KEYBOARDS_RU


def create_keyboard_back():
    buttons = [
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_main_menu'),
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='press_main_menu')
    ]

    keyboard_back_builder = InlineKeyboardBuilder()
    keyboard_back_builder.row(*buttons, width=2)
    return keyboard_back_builder.as_markup()
