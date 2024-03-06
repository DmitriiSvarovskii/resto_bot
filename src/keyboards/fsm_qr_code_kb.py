from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.lexicons import LEXICON_KEYBOARDS_RU


def create_kb_fsm_qr_code() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel_qr'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
