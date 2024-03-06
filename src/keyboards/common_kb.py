from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import LEXICON_KEYBOARDS_RU


def create_kb_del():
    button = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['del_locations'],
        callback_data='press_del')

    keyboard_del_builder = InlineKeyboardBuilder()
    keyboard_del_builder.row(button)
    return keyboard_del_builder.as_markup()


def create_kb_back():
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


def create_kb_fsm_comment() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
