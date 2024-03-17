from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


def create_kb_fsm_edit_openong_hours() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отменить редактирование')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
