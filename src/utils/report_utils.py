from typing import Optional

from src.db import report_db, order_db


async def custom_summary_text(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    custom_sales_summary = await report_db.get_sales_period_summary(
        start_date=start_date,
        end_date=end_date,
    )

    if custom_sales_summary:
        items_summary = [
            f'{item.name_rus} х {item.quantity} шт - {item.unit_price} ₹'
            for item in custom_sales_summary.order_items
        ]
        total_price = (
            f'Итого: {custom_sales_summary.total_price} ₹'
            if items_summary else ''
        )
        message_text = (
            "Продажи за период:\n" +
            '\n'.join(items_summary) + '\n' + total_price
        )
    else:
        message_text = "Отчёт по продажам пуст."
    return message_text


async def create_text_stop_list(store_id: int) -> str:
    response = await report_db.get_stop_list(store_id=store_id)
    order_text = '\n'.join(item.name_rus for item in response)
    return order_text


async def generate_pending_orders_text() -> str:
    order_list = await order_db.get_pending_orders_list()

    message_text = '\n'.join(
        f'- заказ №{items.id} на сумму {items.total_price}'
        for items in order_list
    ) if order_list else "Заказов в очереди нет."

    return message_text


async def generate_delivery_report_text() -> str:
    response = await report_db.get_delivery_report()

    message_text = '\n'.join(
        f'- {items.delivery_area}, количество заказов {items.delivery_count} '
        'на общую сумму {items.total_sales}'
        for items in response
    ) if response else "Отчёт пустой."

    return 'Отчёт продаж по районам доставки:\n' + message_text


async def generate_res_report_text(resourse: str) -> str:
    response = await report_db.get_resourse_report(resourse=resourse)

    if response:
        message_text = (f'Отчёт по каналу рекламы "{resourse}".\n'
                        f'Количество вернувшихся пользователей: {response}')
    else:
        message_text = "Пользователей с этого канала рекламы нет."

    return message_text


async def generate_view_order_text(order_id: int) -> str:
    response = await order_db.get_order_detail(order_id=order_id)
    return f"Заказ № {order_id}:\n" + '\n'.join(
        f'{items.category_name_rus} - {items.name_rus} х '
        f'{items.quantity} шт - {items.unit_price} ₹'
        for items in response
    ) if response else "Такого заказа нет."
