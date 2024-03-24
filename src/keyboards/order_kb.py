from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.lexicons import text_order_ru, text_order_en
from src.utils import OrderStatus
from src.callbacks import (
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,

)


def create_kb_check_order(
    order_type: int,
    order_id: int,
    user_id: int,
    mess_id: int,
    language: str
):
    text_order = (text_order_ru
                  if language == 'ru'
                  else text_order_en)
    buttons = [
        InlineKeyboardButton(
            text=text_order.order_messages_dict['accept_order'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=OrderStatus.ACCEPTED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
        InlineKeyboardButton(
            text=text_order.order_messages_dict['reject_order'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=OrderStatus.CANCELLED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
    ]
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*buttons, width=2)
    return keyboard.as_markup()


def create_kb_time_cooking(
    data: CheckOrdersCallbackFactory,
    mess_id: int,
    language: str,
    time_del: Optional[int] = None,
):
    text_order = (text_order_ru
                  if language == 'ru'
                  else text_order_en)
    keyboard = InlineKeyboardBuilder()

    button_menu = InlineKeyboardButton(
        text=text_order.order_messages_dict['cooking_time'],
        callback_data='press_pass')

    cancel_button = InlineKeyboardButton(
        text=text_order.order_messages_dict['cancelled'],
        callback_data=CheckOrdersCallbackFactory(
            order_type=data.order_type,
            order_id=data.order_id,
            user_id=data.user_id,
            status=OrderStatus.CANCELLED.value['id'],
            mess_id=mess_id,
            language=language
        ).pack()
    )

    button_time_list: list[InlineKeyboardButton] = []

    for time in range(15, 91, 15):
        button_time = InlineKeyboardButton(
            text=f"{time} {text_order.order_messages_dict['time_min']}",
            callback_data=TimeOrdersCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.ACCEPTED.value['id'],
                mess_id=mess_id,
                time=time,
                time_del=time_del,
                language=language
            ).pack()
        )
        button_time_list.append(button_time)

    keyboard.row(button_menu, width=1)

    keyboard.row(*button_time_list, width=3)
    keyboard.row(cancel_button, width=1)

    return keyboard.as_markup()


def create_order_status_keyboard(
    data: TimeOrdersCallbackFactory,
    mess_id: int,
    language: str,
):
    text_order = (text_order_ru
                  if language == 'ru'
                  else text_order_en)
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=text_order.order_messages_dict['ready_for_pickup'],
            callback_data=OrderStatusCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.READY_FOR_PICKUP.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
        InlineKeyboardButton(
            text=text_order.order_messages_dict['cancelled'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.CANCELLED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
        InlineKeyboardButton(
            text=text_order.order_messages_dict['completed'],
            callback_data=OrderStatusCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.COMPLETED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
    ]
    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_order_status_delivery_keyboard(
    mess_id: int,
    data: TimeOrdersCallbackFactory,
    language: str
):
    text_order = (text_order_ru
                  if language == 'ru'
                  else text_order_en)
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=text_order.order_messages_dict['courier_assigned'],
            callback_data=OrderStatusCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.COURIER_ASSIGNED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
        InlineKeyboardButton(
            text=text_order.order_messages_dict['cancelled'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.CANCELLED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
        InlineKeyboardButton(
            text=text_order.order_messages_dict['completed'],
            callback_data=OrderStatusCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.CANCELLED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
    ]
    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_status_redy_order_keyboard(
    data: OrderStatusCallbackFactory,
    mess_id: int,
    language: str
):
    text_order = (text_order_ru
                  if language == 'ru'
                  else text_order_en)
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=text_order.order_messages_dict['cancelled'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.CANCELLED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
        InlineKeyboardButton(
            text=text_order.order_messages_dict['completed'],
            callback_data=OrderStatusCallbackFactory(
                order_type=data.order_type,
                order_id=data.order_id,
                user_id=data.user_id,
                status=OrderStatus.COMPLETED.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        ),
    ]
    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()
