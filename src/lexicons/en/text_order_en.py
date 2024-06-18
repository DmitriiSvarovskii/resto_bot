from datetime import datetime
from typing import List, Optional, Union
from aiogram.types import CallbackQuery

from src.config import TIMEZONE
from src.schemas import (
    cart_schemas,
    customer_schemas,
    delivery_schemas,
    order_schemas
)
from src.utils import OrderTypes
from src.callbacks import (
    TimeOrdersCallbackFactory,
    CheckOrdersCallbackFactory,
    OrderStatusCallbackFactory
)


order_messages_dict: dict[str, str] = {
    'accept_order': 'Accept',
    'reject_order': 'Reject',
    'cooking_time': 'Preparation Time:',
    'time_min': 'min',
    'ready_for_pickup': 'Ready for pickup',
    'cancelled': 'Cancel',
    'completed': 'Completed',
    'courier_assigned': 'Assigned to courier',
}


async def create_order_text(
    cart_items: List[cart_schemas.CartItem]
) -> str:
    order_lines = [
        f'- {cart_item.category_name_en} - {cart_item.name_en} x '
        f'{cart_item.quantity} - {cart_item.unit_price} ₹'
        for cart_item in cart_items
    ]
    return '\n'.join(order_lines)


async def generate_order_messages(
        order_text: str,
        data_order: order_schemas.CreateOrder,
        order_info: Optional[order_schemas.CreateOrderInfo] = None,
        delivery_village: Optional[delivery_schemas.ReadDelivery] = None,
        user_info: Optional[customer_schemas.CustomerBase] = None,
        box_price: Optional[int] = None,
        callback: Optional[CallbackQuery] = None,
):
    current_time = datetime.now(TIMEZONE)
    total_price = data_order.total_price
    sale_price = total_price * 0.9

    user_id = user_info.user_id if user_info else callback.message.chat.id
    first_name = user_info.first_name if user_info else callback.message.chat.first_name  # noqa: E:501
    username = user_info.username if user_info else callback.message.chat.username  # noqa: E:501

    customer_comment = (
        order_info.order_comment
        if order_info.order_comment is not None
        else 'Not provided'
    )

    order_header = (
        f"ORDER №{order_info.order_id} placed on "
        f"{current_time.strftime('%d.%m.%Y')} at "
        f"{current_time.strftime('%H:%M')}\n"
        f"ORDER TYPE: {data_order.order_type}\n"
        "--------------------\n"
    )

    customer_info = (
        "Customer information:\n"
        f"User ID: {user_id}\n"
        f"First Name: {first_name}\n"
        f"Telegram Username: @{username}\n"
        "--------------------\n"
    )

    order_details = (
        "Order Details:\n\n"
        f"{order_text}"
        f"\nOrder Comment: {customer_comment}\n"
        "--------------------"
        f"\nOrder Total: {total_price} ₹\n"
        f'Sale Discount: {total_price * 0.1} ₹\n'
        f"\nTotal Price after Discount: {sale_price} ₹\n"
    )
    if data_order.order_type not in OrderTypes.DINEIN.value.values():
        if box_price and box_price > 0:
            sale_price += box_price
            order_details += (
                f'Additional Box Packing Charge: {box_price} ₹\n'
                "--------------------\n"
            )
    order_details += (
        f'Total Amount Payable: {sale_price} ₹\n'
    )

    chat_text = (
        order_header + customer_info + order_details
    )

    user_text = (
        order_header + order_details
    )

    if data_order.order_type in OrderTypes.DELIVERY.value.values():
        delivery_price = delivery_village.price

        delivery_info = (
            "--------------------\n"
            f"Delivery Charge: {delivery_price} rupees\n"
            f"Total Amount (Order + Delivery): {sale_price + delivery_price} ₹\n"  # noqa: E:501
            "--------------------\n"
            f"Delivery Area: {delivery_village.name_en}\n"
        )

        courier_info = (
            f"Indian Customer Phone Number: {order_info.customer_phone}\n"
            f"Courier Comment: {order_info.delivery_comment}\n"

        )
        if (
            order_info.delivery_latitude
            and
            order_info.delivery_longitude
        ):
            courier_info += (
                "Geolocation will be sent in the next message\n"
            )
        else:
            courier_info += (
                "--------------------\n"
                "<b>User did not provide geolocation. "
                "Please contact the customer for "
                "delivery details clarification\n</b>"
            )

        chat_text += delivery_info + courier_info

        user_text += delivery_info

    status_info = (
        "--------------------\n"
        f"Order Status: {data_order.order_status}\n"

    )

    cancel_text = (
        "--------------------\n"
        '<i>In case of order cancellation, use your personal account. '
        'Order cancellation is available within 15 minutes.\n'
        '(Bot Menu -> Personal Account -> *order number* -> "Cancel ✖️")</i>'
    )

    chat_text += status_info
    user_text += status_info + cancel_text

    return chat_text, user_text


def generate_order_info_time_text(callback_data: TimeOrdersCallbackFactory):
    current_time = datetime.now(TIMEZONE)
    message = (
        "--------------------\n"
        f"Order № {callback_data.order_id} placed on "
        f"{current_time.strftime('%d.%m.%Y')}\n"
        f"Preparation Time: {callback_data.time} minutes\n"
    )
    if callback_data.order_type in OrderTypes.DELIVERY.value.values():
        message += (
            f"Estimated Travel Time: {callback_data.time_del} minutes"
        )
    return message


async def generate_update_order_info_text(
    order_status: str,
    order_id: int,
):
    current_time = datetime.now(TIMEZONE)
    message = (
        "--------------------\n"
        f"Order № {order_id} placed on "
        f"{current_time.strftime('%d.%m.%Y')}\n"
        f"Order Status: {order_status}"
    )
    return message
