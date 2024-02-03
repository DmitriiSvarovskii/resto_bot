from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.services import ORDER_STATUSES
from src.callbacks import (
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,
)


def create_keyboard_back_main():
    button_menu: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['back_menu'],
        callback_data='press_back_main_menu')

    keyboard_back_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_back_builder.add(button_menu,)
    return keyboard_back_builder.as_markup()


def create_keyboard_check_order(
    order_type: int,
    order_id: int,
    user_id: int,
    mess_id: int,
):
    buttons = [
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['accept_order'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['accepted']['id'],
                mess_id=mess_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['reject_order'],
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['cancelled']['id'],
                mess_id=mess_id,
            ).pack()
        ),
    ]
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*buttons, width=2)
    return keyboard.as_markup()


def create_keyboard_time_cooking(
    order_type: int,
    order_id: int,
    user_id: int,
    mess_id: int,
):
    keyboard = InlineKeyboardBuilder()

    button_menu = InlineKeyboardButton(
        text='Время приготовления:',
        callback_data='press_pass')

    cancel_button = InlineKeyboardButton(
        text='Отменить',
        callback_data=CheckOrdersCallbackFactory(
            order_type=order_type,
            order_id=order_id,
            user_id=user_id,
            status=ORDER_STATUSES['cancelled']['id'],
            mess_id=mess_id,
        ).pack()
    )

    button_time_list: list[InlineKeyboardButton] = []

    for time in range(15, 91, 15):
        button_time = InlineKeyboardButton(
            text=f'{time} мин',
            callback_data=TimeOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['accepted']['id'],
                mess_id=mess_id,
                time=time,
            ).pack()
        )
        button_time_list.append(button_time)

    keyboard.row(button_menu, width=1)

    keyboard.row(*button_time_list, width=3)
    keyboard.row(cancel_button, width=1)

    return keyboard.as_markup()


def create_order_status_keyboard(
    order_type: int,
    order_id: int,
    user_id: int,
    mess_id: int,
):
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text='Готов к выдачи',
            callback_data=OrderStatusCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['ready_for_pickup']['id'],
                mess_id=mess_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text='Отменить',
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['cancelled']['id'],
                mess_id=mess_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text='Выполнен',
            callback_data=OrderStatusCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['completed']['id'],
                mess_id=mess_id,
            ).pack()
        ),
    ]
    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_order_status_delivery_keyboard(
    order_type: int,
    order_id: int,
    user_id: int,
    mess_id: int,
):
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text='Передан курьеру',
            callback_data=OrderStatusCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['courier_assigned']['id'],
                mess_id=mess_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text='Отменить',
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['cancelled']['id'],
                mess_id=mess_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text='Выполнен',
            callback_data=OrderStatusCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['completed']['id'],
                mess_id=mess_id,
            ).pack()
        ),
    ]
    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_status_redy_order_keyboard(
    order_type: int,
    order_id: int,
    user_id: int,
    mess_id: int,
):
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text='Отменить',
            callback_data=CheckOrdersCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['cancelled']['id'],
                mess_id=mess_id,
            ).pack()
        ),
        InlineKeyboardButton(
            text='Выполнен',
            callback_data=OrderStatusCallbackFactory(
                order_type=order_type,
                order_id=order_id,
                user_id=user_id,
                status=ORDER_STATUSES['completed']['id'],
                mess_id=mess_id,
            ).pack()
        ),
    ]
    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()
