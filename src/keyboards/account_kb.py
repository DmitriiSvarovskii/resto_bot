from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.services import ORDER_STATUSES
from src.db import order_db, cart_db
from src.callbacks import OrderStatusCallbackFactory


async def create_kb_account(user_id: int):
    order_list = await order_db.get_order_list(user_id=user_id)
    bill_data = await cart_db.get_total_price_cart(user_id=user_id)

    keyboard_build = InlineKeyboardBuilder()

    for item in order_list:

        button = InlineKeyboardButton(
            text='Отменить ✖️',
            callback_data=OrderStatusCallbackFactory(
                order_id=item.id,
                user_id=user_id,
                status=ORDER_STATUSES['cancelled']['id'],
            ).pack()

        )
        if item.order_status == ORDER_STATUSES['completed']['name']:
            button = InlineKeyboardButton(
                text=f'Статус: {item.order_status}',
                callback_data='press_pass'
            )

        keyboard_build.row(
            InlineKeyboardButton(
                text=f'Заказа №{item.id} на сумму {item.total_price} ₹',
                callback_data='test'))
        keyboard_build.row(
            InlineKeyboardButton(text='Подробнее', callback_data='test'),
            button, width=2)
    keyboard_build.row(
        InlineKeyboardButton(
            text='<<< Назад',
            callback_data='press_main_menu'
        ),
        InlineKeyboardButton(
            text=f'Корзина 🛒 {bill_data} ₹',
            callback_data='press_cart'
        ),
        width=2
    )

    return keyboard_build.as_markup()
