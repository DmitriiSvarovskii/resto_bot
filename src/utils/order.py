from typing import List, Optional, Union
from aiogram.types import CallbackQuery

from src.database import get_async_session
from src.services import ORDER_STATUSES
from src.lexicons import new_order_mess_text_order_chat
from src.schemas import (
    CreateOrder,
    CartItem,
    ReadCustomerInfo,
    CreateOrderInfo,
)
from src.callbacks import (
    CheckOrdersCallbackFactory,
    OrderStatusCallbackFactory
)
from src.crud import (
    create_orders,
    crud_read_cart_items_and_totals,
    create_new_order_details,
    read_delivery_one_district,
    create_order_info,
    get_order,
    get_order_info,
    get_order_detail,
    get_user,
    crud_delete_cart_items_by_user_id,
)
from src.fsm_state import user_dict_comment, user_dict
from services.order_constants import ORDER_TYPES
from .cart import get_comment_value, get_user_info


async def create_new_orders(
    order_type: int,
    status: int,
    callback: CallbackQuery,
):
    user_id = callback.message.chat.id

    status_name = await get_status_name_by_id(status)

    type_name = await get_order_type_name_by_id(order_type)

    async for session in get_async_session():
        delivery_village = None

        cart_items = await crud_read_cart_items_and_totals(
            user_id=user_id,
            session=session)

        data_order = await create_data_order(
            user_id=user_id,
            order_type=order_type,
            status=status,
            total_price=cart_items.total_price,
        )

        user_info = get_user_info(
            user_id=user_id,
            user_dict=user_dict
        )

        order_id = await create_orders(
            data_order=data_order,
            session=session
        )

        order_details = await add_order_details(
            order_id=order_id,
            cart_items=cart_items.cart_items
        )

        order_text = await create_order_text(
            cart_items=cart_items.cart_items
        )

        await create_new_order_details(
            data=order_details,
            session=session
        )

        customer_comment = get_comment_value(
            user_id=user_id,
            user_dict_comment=user_dict_comment
        )

        if order_type == ORDER_TYPES['delivery']['id']:
            delivery_village = await read_delivery_one_district(
                delivery_id=user_info['delivery_id'],
                session=session
            )

        data_order_info = await create_data_order_info(
            user_id=user_id,
            order_id=order_id,
            order_comment=customer_comment,
            delivery_id=(user_info.get('delivery_id')
                         if user_info is not None else None),
            customer_phone=(user_info.get('number_phone')
                            if user_info is not None else None),
            delivery_latitude=(user_info.get('latitude')
                               if user_info is not None else None),
            delivery_longitude=(user_info.get('longitude')
                                if user_info is not None else None),
            delivery_comment=(user_info.get('guide')
                              if user_info is not None else None),
        )

        await crud_delete_cart_items_by_user_id(
            user_id=data_order.user_id,
            session=session
        )

        await create_order_info(
            data=data_order_info,
            session=session
        )

        break

    data_customer_info = await create_data_customer_info(
        callback=callback,
    )

    chat_text, user_text = await new_order_mess_text_order_chat(
        order_text=order_text,
        order_sum=cart_items.total_price,
        order_type=type_name,
        status=status_name,
        order_id=order_id,
        data_customer=data_customer_info,
        delivery_village=delivery_village,
        data_order_info=data_order_info,
    )

    return order_id, chat_text, user_text


async def add_order_details(order_id: int, cart_items: List[CartItem]):
    values_list = [
        {
            "order_id": order_id,
            "product_id": detail.product_id,
            "quantity": detail.quantity,
            "unit_price": detail.unit_price
        }
        for detail in cart_items
    ]
    return values_list


async def create_order_text(cart_items: List[CartItem]):
    order_text = ""
    for cart_item in cart_items:
        order_text += (
            f'- {cart_item.category_name} - '
            f'{cart_item.name} x '
            f'{cart_item.quantity} - '
            f'{cart_item.unit_price} ₹\n'
        )
    return order_text


async def create_data_customer_info(
    callback: CallbackQuery,
):
    data_customer_info = ReadCustomerInfo(
        user_id=callback.message.chat.id,
        first_name=callback.message.chat.first_name,
        username=callback.message.chat.username,
    )
    return data_customer_info


async def create_data_order(
    user_id: int,
    total_price: int,
    order_type: int,
    status: int,
):
    status_name = await get_status_name_by_id(status)

    type_name = await get_order_type_name_by_id(order_type)

    data_order = CreateOrder(
        user_id=user_id,
        order_type=type_name,
        order_status=status_name,
        total_price=total_price
    )

    return data_order


async def create_data_order_info(
    user_id: int,
    order_id: int,
    order_comment: Optional[str] = None,
    customer_phone: Optional[str] = None,
    delivery_id: Optional[int] = None,
    delivery_latitude: Optional[float] = None,
    delivery_longitude: Optional[float] = None,
    delivery_comment: Optional[str] = None,
):
    data_order_info = CreateOrderInfo(
        user_id=user_id,
        order_id=order_id,
        order_comment=order_comment,
        customer_phone=customer_phone,
        delivery_id=delivery_id,
        delivery_latitude=delivery_latitude,
        delivery_longitude=delivery_longitude,
        delivery_comment=delivery_comment,
    )

    return data_order_info


async def create_text(
    callback_data: Union[
        CheckOrdersCallbackFactory,
        OrderStatusCallbackFactory,
    ]
):
    async for session in get_async_session():
        delivery_village = None

        order_sum = await get_order(
            order_id=callback_data.order_id,
            session=session
        )

        data_order_info = await get_order_info(
            order_id=callback_data.order_id,
            session=session
        )

        cart_items = await get_order_detail(
            order_id=callback_data.order_id,
            session=session
        )

        data_customer = await get_user(
            user_id=data_order_info.user_id,
            session=session
        )

        if callback_data.order_type == ORDER_TYPES['delivery']['id']:
            delivery_village = await read_delivery_one_district(
                delivery_id=data_order_info.delivery_id,
                session=session
            )

        break

    status_name = await get_status_name_by_id(callback_data.status)

    type_name = await get_order_type_name_by_id(callback_data.order_type)

    order_text = await create_order_text(cart_items=cart_items)

    chat_text, user_text = await new_order_mess_text_order_chat(
        order_text=order_text,
        order_sum=order_sum,
        order_type=type_name,
        status=status_name,
        order_id=callback_data.order_id,
        data_customer=data_customer,
        delivery_village=delivery_village,
        data_order_info=data_order_info,
    )

    return chat_text


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
