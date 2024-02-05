from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
)

from src.callbacks import DeliveryIdCallbackFactory, CreateOrderCallbackFactory
from src.schemas import ReadDelivery
from src.lexicons import LEXICON_KEYBOARDS_RU
from src.services import ORDER_STATUSES, ORDER_TYPES


async def create_keyboard_delivery(delivery_districts: List[ReadDelivery]):
    keyboard = InlineKeyboardBuilder()

    for delivery_district in delivery_districts:

        keyboard.button(
            text=f'{delivery_district.name} - {delivery_district.price} р',
            callback_data=DeliveryIdCallbackFactory(
                delivery_id=delivery_district.id
            )
        )
    keyboard.adjust(2)

    return keyboard.as_markup()


def create_keyboard_delivery_fsm():
    button_1: KeyboardButton = KeyboardButton(
        text=LEXICON_KEYBOARDS_RU['skip'])
    button_2: KeyboardButton = KeyboardButton(
        text=LEXICON_KEYBOARDS_RU['cancel_2'])

    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button_2, button_1]],
        resize_keyboard=True
    )
    return keyboard


def create_keyboard_delivery_fsm_location():
    button_1: KeyboardButton = KeyboardButton(
        text=LEXICON_KEYBOARDS_RU['skip'])
    button_2: KeyboardButton = KeyboardButton(
        text=LEXICON_KEYBOARDS_RU['cancel_2'])
    geo_btn = KeyboardButton(
        text='Отправить геолокацию ✅',
        request_location=True
    )

    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button_2, button_1,], [geo_btn]],
        resize_keyboard=True
    )
    return keyboard


def create_keyboard_delivery_go(mess_id: int):
    button_go_delivery: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['delivery_done'],
        callback_data=CreateOrderCallbackFactory(
            order_type=ORDER_TYPES['delivery']['id'],
            status=ORDER_STATUSES['new']['id'],
            mess_id=mess_id,
        ).pack())
    keyboard_go_delivery_builder = InlineKeyboardBuilder()
    keyboard_go_delivery_builder.row(button_go_delivery)
    return keyboard_go_delivery_builder.as_markup()
