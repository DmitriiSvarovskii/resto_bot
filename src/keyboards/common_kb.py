from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.lexicons import text_main_menu_en, text_main_menu_ru


def create_kb_del(language: str):
    if language == 'ru':
        text_menu = text_main_menu_ru
    else:
        text_menu = text_main_menu_en

    keyboard = InlineKeyboardBuilder()

    row_buttons = [InlineKeyboardButton(
        text=value['text'],
        callback_data=value['callback_data']
    ) for value in text_menu.delete_location_btn.values()]

    keyboard.row(*row_buttons)
    return keyboard.as_markup()


def create_kb_back(language: str):
    if language == 'ru':
        text_menu = text_main_menu_ru
    else:
        text_menu = text_main_menu_en

    text_menu_btn = text_menu.create_navigation_main_btn()

    keyboard = InlineKeyboardBuilder()

    row_buttons = [InlineKeyboardButton(
        text=value['text'],
        callback_data=value['callback_data']
    ) for value in text_menu_btn.values()]

    keyboard.row(*row_buttons, width=2)

    return keyboard.as_markup()


def create_kb_fsm_comment() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
