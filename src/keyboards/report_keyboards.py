from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional, List


from src.lexicons import admin_text
from src.schemas import ReadProduct, GetCategory, GetStore
from src.callbacks import (
    CategoryAdminCallbackFactory,
    ProductIdAdminCallbackFactory,
    CategoryAdminAvailCallbackFactory,
)


def create_keyboard_report():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in admin_text.report_main_dict.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()
