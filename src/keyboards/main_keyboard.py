from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.database import get_async_session
from src.crud import get_user

my_dict = {'menu': {'text': 'menu', 'callback_data': 'press_menu'},
           'contact': {'text': 'contact', 'callback_data': 'press_contact'},
           'menu_2': {'text': 'menu', 'callback_data': 'press_menu'},
           'contact_3': {'text': 'contact', 'callback_data': 'press_contact'}}


# def create_keyboard_main(check_admin: Optional[bool] = None):
#     keyboard = InlineKeyboardBuilder()

#     buttons = []

#     for key, value in my_dict.items():
#         buttons.append(
#             InlineKeyboardButton(
#                 text=value['text'], callback_data=value['callback_data'])
#         )

#     keyboard.row(*buttons, width=2)

#     return keyboard.as_markup()

async def create_keyboard_main(user_id: Optional[int] = None):
    async for session in get_async_session():
        response = await get_user(
            user_id=user_id,
            session=session
        )
        break

    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['menu'],
            callback_data='press_menu'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['contact'],
            callback_data='press_contact'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['delivery'],
            callback_data='press_delivery'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['location'],
            callback_data='press_location'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['personal_account'],
            callback_data='press_personal_account'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['group_telegram'],
            url='https://t.me/PizzaGoaFood'),
    ]
    button_admin = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['admin'],
        callback_data='press_admin')

    keyboard = InlineKeyboardBuilder()

    keyboard.row(*buttons, width=2)

    if response.admin:
        keyboard.row(button_admin, width=1)

    return keyboard.as_markup()
