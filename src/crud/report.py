from datetime import datetime
from sqlalchemy import desc, select, cast, Date
from sqlalchemy.orm import Query
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from ..models import (
    Product,
    Order,
    OrderDetail,
    OrderInfo,
    Delivery,
    Customer,
)
from ..schemas import (
    SalesSummary,
    SalesSummaryList,
    OrderList,
    DeliveryReport,
    CustomerAdResourse,
)


async def create_main_query():
    return (
        select(
            Product.id,
            Product.category_id,
            Product.name,
            func.sum(OrderDetail.quantity).label('quantity'),
            func.sum(OrderDetail.unit_price).label('unit_price')
        )
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .join(Order, Order.id == OrderDetail.order_id)
        .group_by(Product.id, Product.category_id, Product.name)
        .order_by(Product.id)
    )


async def create_total_price_query():
    return (
        select(
            func.sum(OrderDetail.unit_price).over().label("total_price"))
        .join(Order, Order.id == OrderDetail.order_id)
        .where(Order.order_status == "Выполнен")
    )


# async def crud_get_daily_sales_summary(
#         session: AsyncSession,
#         canceled: Optional[str] = None,
#         start_date: Optional[str] = None,
#         end_date: Optional[str] = None,
#         filter=None,
# ) -> List[SalesSummary]:
#     pass


async def crud_get_sales_period_summary(
        session: AsyncSession,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
) -> Optional[SalesSummaryList]:
    query = await create_main_query()
    query_total_price = await create_total_price_query()

    query, query_total_price = await apply_date_filters(
        query=query,
        query_total_price=query_total_price,
        start_date=start_date,
        end_date=end_date
    )

    result = await session.execute(query)
    result_total_price = await session.execute(query_total_price)
    total_price = result_total_price.scalar()

    sales_summary = [SalesSummary(**row._asdict()) for row in result]
    if sales_summary and total_price:
        sales_summary_list = SalesSummaryList(
            order_items=sales_summary,
            total_price=total_price
        )

        return sales_summary_list
    else:
        return None


async def crud_get_pending_orders_list(
        session: AsyncSession,
) -> List[OrderList]:
    query = (
        select(Order)
        .where(Order.order_status != "Выполнен",
               Order.order_status != "Отменён")
        .order_by(Order.id)
    )

    result = await session.execute(query)
    return result.scalars().all()


async def crud_get_order_by_number(
        session: AsyncSession,
        order_number: int,
) -> Order:
    pass


async def crud_get_delivery_report(
        session: AsyncSession,
) -> List[DeliveryReport]:
    query = (
        select(
            Delivery.name.label('delivery_area'),
            func.count(OrderInfo.id).label('delivery_count'),
            func.sum(Order.total_price).label('total_sales')
        )
        .join(OrderInfo, OrderInfo.delivery_id == Delivery.id)
        .join(Order, OrderInfo.order_id == Order.id)
        .group_by(Delivery.name)
        .order_by(desc(func.sum(Order.total_price)))
    )

    result = await session.execute(query)

    return result.all()


# async def crud_get_advertising_report(
#         session: AsyncSession,
#         start_date: Optional[str] = None,
#         end_date: Optional[str] = None,
# ) -> List[AdvertisingReport]:
#     pass


async def apply_date_filters(
    query: Query,
    query_total_price: Query,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):

    if start_date or end_date:
        converted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        converted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        date_condition = (
            (cast(OrderDetail.created_at, Date) >= converted_start_date) &
            (cast(OrderDetail.created_at, Date) <= converted_end_date)
        )

        query = query.where(Order.order_status == "Выполнен", date_condition)
        query_total_price = query_total_price.where(
            Order.order_status == "Выполнен", date_condition)

    return query, query_total_price


async def apply_filters(
    query,
    query_total_price,
    canceled,
    filter,
    start_date,
    end_date
):
    if canceled:
        query = query.where(Order.order_status == canceled)
        query_total_price = query_total_price.where(
            Order.order_status == canceled)
    if filter:
        query = query.where(Order.order_status == "Выполнен",
                            OrderDetail.order_id == filter)
        query_total_price = query_total_price.where(
            Order.order_status == "Выполнен", OrderDetail.order_id == filter)

    if start_date and end_date:
        converted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        converted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        date_condition = (
            (cast(OrderDetail.created_at, Date) >= converted_start_date) &
            (cast(OrderDetail.created_at, Date) <= converted_end_date)
        )
        query = query.where(Order.order_status == "Выполнен", date_condition)
        query_total_price = query_total_price.where(
            Order.order_status == "Выполнен", date_condition)

    return query, query_total_price


async def crud_get_daily_sales(
        session: AsyncSession,
        canceled: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        filter=None,
) -> List[SalesSummary]:
    query = await create_main_query()
    query_total_price = await create_total_price_query()
    query, query_total_price = await apply_filters(
        query,
        query_total_price,
        canceled,
        filter,
        start_date,
        end_date
    )

    result = await session.execute(query)
    result_total_price = await session.execute(query_total_price)
    total_price = result_total_price.scalar()

    sales_summary = [SalesSummary(**row._asdict()) for row in result]
    if sales_summary and total_price:
        sales_summary_list = SalesSummaryList(
            order_items=sales_summary,
            total_price=total_price
        )

        return sales_summary_list
    else:
        return None

# async def crud_get_daily_sales(
#         session: AsyncSession,
#         canceled: Optional[str] = None,
#         start_date: Optional[str] = None,
#         end_date: Optional[str] = None,
#         filter=None,
# ) -> List[SalesSummary]:
#     query = (
#         select(
#             Product.id,
#             Product.category_id,
#             Product.name,
#             func.sum(OrderDetail.quantity).label('quantity'),
#             func.sum(OrderDetail.unit_price).label('unit_price')
#         )
#         .join(OrderDetail, OrderDetail.product_id == Product.id)
#         .join(Order, Order.id == OrderDetail.order_id)
#         # .where(Order.order_status == "Выполнен")
#         .group_by(Product.id, Product.category_id, Product.name)
#         .order_by(Product.id)
#     )

#     query_total_price = (select(
#         func.sum(OrderDetail.unit_price).over().label("total_price"))
#         .join(Order, Order.id == OrderDetail.order_id)
#         .where(Order.order_status == "Выполнен")
#     )

#     if canceled:
#         query = query.where(Order.order_status == canceled)
#         query_total_price = query_total_price.where(
#             Order.order_status == canceled)
#     if filter:
#         query = query.where(Order.order_status == "Выполнен",
#                             OrderDetail.order_id == filter)
#         query_total_price = query_total_price.where(
#             Order.order_status == "Выполнен",
#             OrderDetail.order_id == filter
#         )

#     if start_date and end_date:
#         converted_start_date = datetime.strptime(
    # start_date, '%Y-%m-%d'
    # ).date()
#         converted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#         date_condition = (
#             (cast(OrderDetail.created_at, Date) >= converted_start_date) &
#             (cast(OrderDetail.created_at, Date) <= converted_end_date)
#         )
#         query = query.where(Order.order_status == "Выполнен", date_condition)
#         query_total_price = query_total_price.where(
#             Order.order_status == "Выполнен", date_condition)

#     result = await session.execute(query)
#     result_total_price = await session.execute(query_total_price)
#     total_price = result_total_price.scalar()


#     sales_summary = [SalesSummary(**row._asdict()) for row in result]
#     if sales_summary and total_price:
#         sales_summary_list = SalesSummaryList(
#             order_items=sales_summary,
#             total_price=total_price
#         )

#         return sales_summary_list
#     else:
#         return None


async def crud_get_ad_report(
        resourse: str,
        session: AsyncSession,
) -> List[CustomerAdResourse]:
    query = (
        select(
            func.count(Customer.id).label('customer_count')
        )
        .where(Customer.resourse == resourse)
        .order_by(desc(func.count(Customer.id).label('customer_count')))
    )

    result = await session.execute(query)
    response = result.scalar()
    return response
