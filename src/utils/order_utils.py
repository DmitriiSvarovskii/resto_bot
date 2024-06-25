from typing import List, Union
from aiogram.types import CallbackQuery

from src.callbacks.order import OrderCallbackFactory
from src.db import cart_db, order_db, delivery_db, customer_db
from src.services import ORDER_STATUSES
from src.lexicons import text_order_ru, text_order_en
from src.schemas import order_schemas, customer_schemas, cart_schemas
from src.services.order_constants import ORDER_TYPES
from src.callbacks import (
    CheckOrdersCallbackFactory,
    OrderStatusCallbackFactory,
)
from .order_constants import OrderTypes, OrderStatus
from .redis_utils import get_data_from_redis


async def create_new_orders(
    callback: CallbackQuery,
    callback_data: OrderCallbackFactory,
    language: str
):
    text_order = text_order_ru if language == 'ru' else text_order_en

    user_id = callback.message.chat.id

    delivery_data = await get_data_from_redis(
        key_prefix='delivery_comment',
        user_id=user_id
    )

    order_comment = await get_data_from_redis(
        key_prefix='order_comment',
        user_id=user_id
    )

    cart_items = await cart_db.get_cart_items_and_totals(
        user_id=user_id,
        store_id=callback_data.store_id
    )

    data_order = await create_data_order(
        user_id=user_id,
        callback_data=callback_data,
        total_price=cart_items.total_price,
        language=language,
    )

    order_id = await order_db.create_orders(
        data_order=data_order
    )

    order_details = await add_order_details(
        order_id=order_id,
        cart_items=cart_items.cart_items
    )

    await order_db.create_new_order_details(
        data=order_details,
    )

    order_text = await text_order.create_order_text(
        cart_items=cart_items.cart_items
    )

    box_price = create_box_price(
        cart_items=cart_items.cart_items
    )

    if delivery_data is not None:
        order_info_data = {**{'user_id': user_id,
                              'order_id': order_id}, **delivery_data}
        order_info = order_schemas.CreateOrderInfo(**order_info_data)
    else:
        order_info = order_schemas.CreateOrderInfo(
            user_id=user_id, order_id=order_id)

    if order_comment is not None:
        for key, value in order_comment.items():
            setattr(order_info, key, value)

    await order_db.create_order_info(
        data=order_info
    )

    delivery_village = (
        await delivery_db.get_delivery_one_district(
            delivery_id=order_info.delivery_id,
            store_id=callback_data.store_id
        ) if callback_data.order_type in OrderTypes.DELIVERY.value.values()
        else None)

    await cart_db.delete_cart_items_by_user_id(
        user_id=user_id,
        store_id=callback_data.store_id
    )

    chat_text, user_text = await text_order.generate_order_messages(
        order_text=order_text,
        data_order=data_order,
        callback=callback,
        delivery_village=delivery_village,
        order_info=order_info,
        box_price=box_price,
    )
    return order_info, chat_text, user_text


async def create_text(
    callback_data: Union[
        CheckOrdersCallbackFactory,
        OrderStatusCallbackFactory,
    ],
    language: str
):
    text_order = text_order_ru if language == 'ru' else text_order_en

    order_id = callback_data.order_id

    data_order = await order_db.get_order(order_id=order_id)

    user_info = await customer_db.get_user_info_by_id(user_id=data_order.user_id)  # noqa: E:501

    order_info = await order_db.get_order_info(order_id=order_id)

    cart_items = await order_db.get_order_detail(order_id=order_id)

    delivery_village = (await delivery_db.get_delivery_one_district(
        delivery_id=order_info.delivery_id,
        store_id=callback_data.store_id
    ) if callback_data.order_type in OrderTypes.DELIVERY.value.values()
        else None)

    order_text = await text_order.create_order_text(cart_items=cart_items)

    box_price = sum(item.box_price or 0 for item in cart_items)

    chat_text, user_text = await text_order.generate_order_messages(
        order_text=order_text,
        data_order=data_order,
        user_info=user_info,
        delivery_village=delivery_village,
        order_info=order_info,
        box_price=box_price
    )

    return chat_text


async def create_order_messages_id(
    order_id: int,
    message_id: int
):
    data = order_schemas.CreateOrderMessageId(
        order_id=order_id, message_id=message_id)
    await order_db.db_create_order_messages_id(data)


async def create_data_order(
    user_id: int,
    total_price: int,
    language: str,
    callback_data: OrderCallbackFactory,
):
    order_type = OrderTypes.get_name_by_id(
        target_id=callback_data.order_type,
        language=language
    )
    order_status = OrderStatus.get_name_by_id(
        target_id=callback_data.status,
        language=language
    )

    data_order = order_schemas.CreateOrder(
        user_id=user_id,
        order_type=order_type,
        order_status=order_status,
        total_price=total_price,
        store_id=callback_data.store_id
    )

    return data_order


async def add_order_details(
    order_id: int,
    cart_items: List[cart_schemas.CartItem]
):
    data = [
        {
            "order_id": order_id,
            "product_id": detail.product_id,
            "quantity": detail.quantity,
            "unit_price": detail.unit_price
        }
        for detail in cart_items
    ]
    return data


def create_box_price(
    cart_items: List[cart_schemas.CartItem]
):
    return sum(item.box_price or 0 for item in cart_items)


async def create_data_customer_info(
    callback: CallbackQuery,
):
    data_customer_info = customer_schemas.ReadCustomerInfo(
        user_id=callback.message.chat.id,
        first_name=callback.message.chat.first_name,
        username=callback.message.chat.username,
    )
    return data_customer_info


async def create_order_text(
    cart_items: List[cart_schemas.CartItem],
) -> str:
    order_lines = [
        f'- {cart_item.category_name} - {cart_item.name} x '
        f'{cart_item.quantity} - {cart_item.unit_price} ₹'
        for cart_item in cart_items
    ]
    return '\n'.join(order_lines)


async def get_status_name_by_id(status_id: int) -> str:
    for status_name, status_info in ORDER_STATUSES.items():
        if status_info['id'] == status_id:
            return status_info['name']

    raise ValueError(f"Status with id {status_id} not found in ORDER_STATUSES")


async def get_order_type_name_by_id(type_id: int) -> str:
    for type_name, type_info in ORDER_TYPES.items():
        if type_info['id'] == type_id:
            return type_info['name']

    raise ValueError(f"Order type with id {type_id} not found in ORDER_TYPES")
