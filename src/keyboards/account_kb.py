from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db import order_db, cart_db
from src.utils import OrderStatus, time_utils
from src.callbacks import (
    OrderStatusCallbackFactory,
    AccountOrdersCbData,
    StoreCbDataList,
    CartCallbackData
)


async def create_kb_account(
    user_id: int,
    language: str,
    store_id: int
):
    order_list = await order_db.get_order_list(user_id=user_id)
    bill_data = await cart_db.get_total_price_cart(user_id=user_id,
                                                   store_id=store_id)

    keyboard_build = InlineKeyboardBuilder()

    for item in order_list:
        mess_id = item.message_id if item.message_id else 1
        button = InlineKeyboardButton(
            text='Отменить ✖️',
            callback_data=OrderStatusCallbackFactory(
                type_callback='cancel-acc',
                order_id=item.id,
                user_id=user_id,
                status=OrderStatus.CANCELLED.value['id'],
                mess_id=mess_id,
                store_id=store_id,
                language=language
            ).pack()

        )

        if not await time_utils.check_time(item.created_at):
            button = InlineKeyboardButton(
                text=f'Статус: {item.order_status}',
                callback_data='press_pass'
            )
        if (item.order_status in OrderStatus.COMPLETED.value.values() or
                item.order_status in OrderStatus.CANCELLED.value.values()):

            button = InlineKeyboardButton(
                text=f'Статус: {item.order_status}',
                callback_data='press_pass'
            )
        keyboard_build.row(
            InlineKeyboardButton(
                text=f'Заказа №{item.id} на сумму {item.total_price} ₹',
                callback_data='test'))
        keyboard_build.row(
            InlineKeyboardButton(
                text='Подробнее',
                callback_data=AccountOrdersCbData(
                    type_callback='order-details',
                    order_id=item.id,
                    user_id=user_id,
                ).pack()
            ),
            button, width=2)
    keyboard_build.row(
        InlineKeyboardButton(
            text='<<< Назад',
            callback_data=StoreCbDataList(
                store_id=store_id,
                type_press='select-one'
            ).pack()
        ),
        InlineKeyboardButton(
            text=f'Корзина 🛒 {bill_data} ₹',
            callback_data=CartCallbackData(
                store_id=store_id,
                type_press='cart'
            ).pack()
        ),
        width=2
    )

    return keyboard_build.as_markup()
