from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..lexicons import LEXICON_KEYBOARDS_RU


def create_keyboard_del():
    button = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['del_locations'],
        callback_data='press_del')

    keyboard_del_builder = InlineKeyboardBuilder()
    keyboard_del_builder.row(button)
    return keyboard_del_builder.as_markup()
