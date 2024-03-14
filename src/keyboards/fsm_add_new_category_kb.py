from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
)

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.callbacks import (
    AddCategoryAvailabilityCallbackFactory
)


def create_kb_approval():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='press_approval_cat')
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Внести изменения',
            callback_data='press_make_changes_cat')
    )

    return keyboard.as_markup()


def create_kb_availability():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='В наличии',
            callback_data=AddCategoryAvailabilityCallbackFactory(
                availability=True
            ).pack()
        ),
        InlineKeyboardButton(
            text='Отсутствует',
            callback_data=AddCategoryAvailabilityCallbackFactory(
                availability=False
            ).pack()
        )
    )

    return keyboard.as_markup()


def create_kb_fsm_canel() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text=LEXICON_KEYBOARDS_RU['cancel_add_category'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
