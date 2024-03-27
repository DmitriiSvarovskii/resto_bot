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

# special_offer_dict: dict[str, dict[str, str]] = {
#     'time_cooking': {
#         'text': 'Время приготовления:',
#         'callback_data': 'press_pass'
#     }
# }


order_messages_dict: dict[str, str] = {
    'accept_order': 'Принять',
    'reject_order': 'Отклонить',
    'cooking_time': 'Время приготовления:',
    'time_min': 'мин',
    'ready_for_pickup': 'Готов к выдачи',
    'cancelled': 'Отменить',
    'completed': 'Выполнен',
    'courier_assigned': 'Передан курьеру',
}


async def create_order_text(
    cart_items: List[cart_schemas.CartItem]
) -> str:
    order_lines = [
        f'- {cart_item.category_name_rus} - {cart_item.name_rus} x '
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
    sale_price = total_price*0.95

    user_id = user_info.user_id if user_info else callback.message.chat.id
    first_name = user_info.first_name if user_info else callback.message.chat.first_name  # noqa: E501
    username = user_info.username if user_info else callback.message.chat.username  # noqa: E501

    customer_comment = (
        order_info.order_comment
        if order_info.order_comment is not None
        else 'Отсутствует'
    )

    order_header = (
        f"ЗАКАЗ №{order_info.order_id} от "
        f"{current_time.strftime('%d.%m.%Y')} в "
        f"{current_time.strftime('%H:%M')}\n"
        f"ТИП ЗАКАЗА: {data_order.order_type}\n"
        "--------------------\n"
    )

    customer_info = (
        "Информация о клиенте:\n"
        f"Код клиента: {user_id}\n"
        f"Имя клиента: {first_name}\n"
        f"Ссылка tg: @{username}\n"
        "--------------------\n"
    )

    order_details = (
        "Заказ:\n\n"
        f"{order_text}"
        f"\nКомментарий к заказу: {customer_comment}\n"
        "--------------------"
        f"\nСумма заказа: {total_price} ₹\n"
        f'Скидка: {total_price*0.05} ₹\n'
        f"\nСумма заказа с учётом скидки: {sale_price} ₹\n"
    )
    if box_price and box_price > 0:
        sale_price += box_price
        order_details += (
            f'Дополнительная плата за упаковку: {box_price} ₹\n'
            "--------------------\n"
            f'Итоговая сумма к оплате:: {sale_price} ₹\n'
        )

    chat_text = (
        order_header + customer_info + order_details
    )

    user_text = (
        order_header + order_details
    )
    print(OrderTypes.DELIVERY.value['id'])
    print(data_order.order_type)
    if data_order.order_type in OrderTypes.DELIVERY.value.values():
        delivery_price = delivery_village.price

        delivery_info = (
            "--------------------\n"
            f"Стоимость доставки: {delivery_price} руп.\n"
            f"Итого (заказ + доставка): {sale_price + delivery_price} ₹\n"
            "--------------------\n"
            f"Район доставки: {delivery_village.name_rus}\n"
        )

        courier_info = (
            f"Индийский номер клиента: {order_info.customer_phone}\n"
            f"Комментарий для курьера: {order_info.delivery_comment}\n"

        )
        if (
            order_info.delivery_latitude
            and
            order_info.delivery_longitude
        ):
            courier_info += (
                "Геолокация будет отправлена следующим сообщением\n"
            )
        else:
            courier_info += (
                "--------------------\n"
                "<b>Пользователь не прикрепил геолокацию. "
                "Пожалуйста свяжитесь с клиентом для "
                "уточнения деталей доставки\n</b>"
            )

        chat_text += delivery_info + courier_info

        user_text += delivery_info

    status_info = (
        "--------------------\n"
        f"Статус заказа: {data_order.order_status}\n"

    )

    cancel_text = (
        "--------------------\n"
        '<i>В случае отмены заказа воспользуйтесь личным кабинетом. '
        'Отмена заказа доступна в течении 15 минут.\n'
        '(Меню бота -> Личный кабинет -> *номер заказа* -> "Отменить ✖️")</i>'
    )

    chat_text += status_info
    user_text += status_info + cancel_text

    return chat_text, user_text


def generate_order_info_time_text(callback_data: TimeOrdersCallbackFactory):
    current_time = datetime.now(TIMEZONE)
    message = (
        "--------------------\n"
        f"Заказ № {callback_data.order_id} от "
        f"{current_time.strftime('%d.%m.%Y')}\n"
        f"Время приготовления: {callback_data.time} минут\n"
    )
    if callback_data.order_type in OrderTypes.DELIVERY.value.values():
        message += (
            f"Ориентировочное время поездки: {callback_data.time_del} минут"
        )
    return message


async def generate_update_order_info_text(
    order_status: str,
    order_id: int,
):
    current_time = datetime.now(TIMEZONE)
    message = (
        "--------------------\n"
        f"Заказ № {order_id} от "
        f"{current_time.strftime('%d.%m.%Y')}\n"
        f"Статус заказа: {order_status}"
    )
    return message
