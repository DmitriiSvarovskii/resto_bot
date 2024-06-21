from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import admin_text


def create_kb_report(store_id: int):
    keyboard = InlineKeyboardBuilder()
    report_main_btn = admin_text.create_report_main_btn(store_id=store_id)
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for key, value in report_main_btn.items()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()
