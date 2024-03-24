from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.lexicons import (
    text_common_ru,
    text_common_en,
    text_fsm_delivery_ru,
    text_fsm_delivery_en,
)


# def create_kb_fsm_comment() -> ReplyKeyboardMarkup:
#     button = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel'])
#     keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
#         keyboard=[[button]],
#         resize_keyboard=True
#     )
#     return keyboard


def create_kb_fsm_comment(language: str):
    text_common = (text_common_ru
                   if language == 'ru'
                   else text_common_en)
    buttons = [
        [KeyboardButton(text=text_common.common_dict['cancel'])]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
