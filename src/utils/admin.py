from typing import Optional
from datetime import datetime

from src.database import get_async_session
from src.crud import (
    get_order_detail_test,
    crud_get_sales_period_summary,
    crud_get_stop_list,
    crud_get_store_info,
    crud_get_all_categories,
    crud_get_pending_orders_list,
    crud_get_delivery_report,
    crud_get_ad_report,
)
from src.keyboards import (
    create_keyboard_toggle_bot,
    create_keyboard_category_avail_admin,
    create_keyboard_category_admin,
)


async def get_stop_list() -> None:
    async for session in get_async_session():
        response = await crud_get_stop_list(
            session=session
        )
        break

    order_text = ''
    for item in response:
        order_text += (
            f'{item.name}\n'
        )
    return order_text


async def generate_sales_summary_text() -> str:
    async for session in get_async_session():
        sales_summary = await crud_get_sales_period_summary(
            start_date=datetime.now().strftime('%Y-%m-%d'),
            end_date=datetime.now().strftime('%Y-%m-%d'),
            session=session
        )
        break

    if sales_summary:
        message_text = "Продажи за сегодня:\n"
        for items in sales_summary.order_items:
            message_text += (
                f'{items.name} х {items.quantity} шт - {items.unit_price} ₹\n'
            )

        message_text += f'Итого: {sales_summary.total_price} ₹'

    else:
        message_text = "Сегодня продаж нет."

    return message_text


async def generate_custom_sales_summary_text(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    async for session in get_async_session():
        custom_sales_summary = await crud_get_sales_period_summary(
            start_date=start_date,
            end_date=end_date,
            session=session
        )
        break

    if custom_sales_summary:
        message_text = "Продажи за период:\n"
        for items in custom_sales_summary.order_items:
            message_text += (
                f'{items.name} х {items.quantity} шт - {items.unit_price} ₹\n'
            )

        message_text += f'Итого: {custom_sales_summary.total_price} ₹'

    else:
        message_text = "За выбранный период продаж нет."

    return message_text


async def generate_pending_orders_text() -> str:
    async for session in get_async_session():
        pending_orders = await crud_get_pending_orders_list(session=session)
        break

    if pending_orders:
        message_text = 'Очередь заказов:\n'
        for items in pending_orders:
            message_text += (
                f'- заказ №{items.id} на сумму {items.total_price}\n'
            )
    else:
        message_text = "Заказов в очереди нет."

    return message_text


async def generate_delivery_report_text() -> str:
    async for session in get_async_session():
        delivery_report = await crud_get_delivery_report(session=session)
        break

    if delivery_report:
        message_text = 'Отчёт продаж по районам доставки:\n'
        for items in delivery_report:
            message_text += (
                f'- {items.delivery_area}, '
                f'количество заказов {items.delivery_count} '
                f'на общую сумму {items.total_sales}\n'
            )
    else:
        message_text = "Отчёт пустой."

    return message_text


async def generate_view_order_text(order_id: int) -> str:
    async for session in get_async_session():
        order_text = await get_order_detail_test(
            order_id=order_id,
            session=session
        )
        break

    if order_text:
        message_text = f"Заказ № {order_id}:\n"
        for items in order_text:
            message_text += (
                f'{items.category_name} - '
                f'{items.name} х '
                f'{items.quantity} шт - '
                f'{items.unit_price} ₹\n'
            )

    else:
        message_text = "Такого заказа нет."

    return message_text


async def generate_ad_report_text(resourse: str) -> str:
    async for session in get_async_session():
        ad_report = await crud_get_ad_report(
            resourse=resourse,
            session=session
        )
        break

    if ad_report:
        message_text = str(ad_report)

    else:
        message_text = "Пользователей с этой рекламы нет."

    return message_text


async def generate_categories_admin():
    async for session in get_async_session():
        categories = await crud_get_all_categories(session=session)
        keyboard = await create_keyboard_category_admin(
            categories=categories
        )
        break
    return keyboard


async def generate_categories_avail_admin():
    async for session in get_async_session():
        categories = await crud_get_all_categories(session=session)
        keyboard = await create_keyboard_category_avail_admin(
            categories=categories
        )
        break
    return keyboard


async def get_store_info():
    async for session in get_async_session():
        store_info = await crud_get_store_info(session=session)

        keyboard = create_keyboard_toggle_bot(
            store_info=store_info
        )
        break
    return keyboard
