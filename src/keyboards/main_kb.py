from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import text_main_menu_ru, text_main_menu_en
from src.db import customer_db


async def create_kb_main(language: str, user_id):
    user_info = await customer_db.get_user_info_by_id(user_id=user_id)

    keyboard = InlineKeyboardBuilder()

    if language == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    buttons = []

    for key, value in text_main_menu.main_btn.items():
        if 'admin' in key and not user_info.admin:
            continue
        if 'callback_data' in value:
            button = InlineKeyboardButton(
                text=value['text'], callback_data=value['callback_data'])
        elif 'url' in value:
            button = InlineKeyboardButton(
                text=value['text'], url=value['url'])
        buttons.append(button)

    keyboard.row(*buttons, width=2)

    return keyboard.as_markup()
