from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.schemas import store_schemas
from src.callbacks import (
    StoreCbData,
)


def create_kb_toggle_bot(store_info: Optional[store_schemas.GetStore]):
    keyboard = InlineKeyboardBuilder()

    is_active = "Работает" if store_info.is_active else "Выключён"
    indicator = '✅' if store_info.is_active else '❌'
    action = "Выключить" if store_info.is_active else "Включить"

    keyboard.row(
        InlineKeyboardButton(
            text=f'{store_info.name}',
            callback_data='press_toggle_working_bot')
    )

    keyboard.row(
        InlineKeyboardButton(
            text=is_active,
            callback_data='press_toggle_working_bot'),
        InlineKeyboardButton(
            text=indicator,
            callback_data='press_toggle_working_bot'),
        InlineKeyboardButton(
            text=action,
            callback_data='press_toggle_working_bot'),
        width=3
    )

    keyboard.row(
        InlineKeyboardButton(
            text='Режим работы',
            callback_data='press_pass'))
    keyboard.row(
        InlineKeyboardButton(
            text=f'с {store_info.opening_time.strftime("%H:%M")} до {store_info.closing_time.strftime("%H:%M")}',
            callback_data='press_pass'),
        InlineKeyboardButton(
            text='Редактировать',
            callback_data='press_edit_hours'),
        width=2
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Редактировать локацию',
            callback_data=StoreCbData(
                store_id=store_info.id,
                type_update='location'
            ).pack())
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Редактировать текст-приветствие',
            callback_data=StoreCbData(
                store_id=store_info.id,
                type_update='welcome-text'
            ).pack())
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Изменить менеджерскую группу',
            callback_data=StoreCbData(
                store_id=store_info.id,
                type_update='manager-group'
            ).pack())
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Изменить клиентскую группу',
            callback_data=StoreCbData(
                store_id=store_info.id,
                type_update='sale-group'
            ).pack())
    )
    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_admin'
        )
    )

    return keyboard.as_markup()
