from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

from src.lexicons import text_main_menu_ru, text_main_menu_en
from src.db import customer_db
from src.schemas import store_schemas
from src.callbacks import StoreCbDataList


async def create_kb_select_store(
    language: str,
    store_list: List[store_schemas.GetStore]
):
    keyboard = InlineKeyboardBuilder()

    if language == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    for store in store_list:
        keyboard.row(
            InlineKeyboardButton(
                text=store.name,
                callback_data=StoreCbDataList(
                    store_id=store.id,
                    type_press='select-one'
                ).pack()))

    return keyboard.as_markup()


# async def create_kb_main(language: str, user_id: int, store_id: int):
#     user_info = await customer_db.get_user_info_by_id(user_id=user_id)

#     keyboard = InlineKeyboardBuilder()

#     if language == 'ru':
#         text_main_menu = text_main_menu_ru
#     else:
#         text_main_menu = text_main_menu_en

#     buttons = []

#     for key, value in text_main_menu.main_btn.items():
#         if 'admin' in key and not user_info.admin:
#             continue
#         if 'callback_data' in value:
#             button = InlineKeyboardButton(
#                 text=value['text'], callback_data=value['callback_data'])
#         elif 'url' in value:
#             button = InlineKeyboardButton(
#                 text=value['text'], url=value['url'])
#         buttons.append(button)

#     keyboard.row(*buttons, width=2)

#     return keyboard.as_markup()


async def create_kb_main(
    language: str,
    user_id: int,
    store_id: int
):
    user_info = await customer_db.get_user_info_by_id(user_id=user_id)

    keyboard = InlineKeyboardBuilder()

    if language == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    menu_btn = text_main_menu.create_main_btn(store_id=store_id)

    buttons = []

    for key, value in menu_btn.items():
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
