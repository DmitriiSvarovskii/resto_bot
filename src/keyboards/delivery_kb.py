from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
)

from src.callbacks import DeliveryIdCallbackFactory, CreateOrderCallbackFactory
from src.schemas import delivery_schemas
from src.lexicons import (
    text_common_ru,
    text_common_en,
    text_fsm_delivery_ru,
    text_fsm_delivery_en,
)
from src.utils import OrderStatus, OrderTypes


async def create_kb_delivery(
    delivery_districts: List[delivery_schemas.ReadDelivery],
    language: str
):
    keyboard = InlineKeyboardBuilder()

    for delivery_district in delivery_districts:
        district_name = (delivery_district.name_rus
                         if language == 'ru'
                         else delivery_district.name_en)
        keyboard.button(
            text=f'{district_name} - {delivery_district.price} ',
            callback_data=DeliveryIdCallbackFactory(
                delivery_id=delivery_district.id
            )
        )
    keyboard.adjust(2)

    return keyboard.as_markup()


def create_kb_delivery_fsm(language: str):
    text_common = (text_common_ru
                   if language == 'ru'
                   else text_common_en)
    buttons = [
        [KeyboardButton(text=text_common.common_dict['cancel']),
         KeyboardButton(text=text_common.common_dict['skip'])]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return keyboard


def create_kb_delivery_fsm_location(language: str):
    text_common, text_delivery = (text_common_ru, text_fsm_delivery_ru) if language == 'ru' else (
        text_common_en, text_fsm_delivery_en)

    buttons = [
        [KeyboardButton(text=text_common.common_dict['cancel']),
         KeyboardButton(text=text_common.common_dict['skip'])],
        [KeyboardButton(
            text=text_delivery.delivery_fsm_text['send_location'],
            request_location=True
        )]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def create_kb_delivery_go(mess_id: int, language: str):
    text_delivery = (text_fsm_delivery_ru
                     if language == 'ru'
                     else text_fsm_delivery_en)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text=text_delivery.delivery_fsm_text['confirm_delivery'],
            callback_data=CreateOrderCallbackFactory(
                type_callback='create',
                order_type=OrderTypes.DELIVERY.value['id'],
                status=OrderStatus.NEW.value['id'],
                mess_id=mess_id,
                language=language,
            ).pack()
        )
    )

    return keyboard.as_markup()
