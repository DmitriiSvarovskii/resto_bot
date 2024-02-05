from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.schemas import (
    CreateOrder,
    CreateOrderDetail,
    CreateOrderInfo,
    GetOrder,
    CartItem,
    OrderDetailTest
)
from src.models import (
    Category,
    Product,
    Order,
    OrderDetail,
    OrderInfo
)


async def create_orders(
    data_order: CreateOrder,
    session: AsyncSession,
):
    stmt_order = (
        insert(Order).
        values(**data_order.dict()).
        returning(Order.id)
    )
    result = await session.execute(stmt_order)

    await session.commit()

    order_id = result.scalar()

    return order_id


async def create_new_order_details(
    data: List[CreateOrderDetail],
    session: AsyncSession,
):
    stmt = (
        insert(OrderDetail).
        values(data)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Order created successfully"}


async def create_order_info(
    data: CreateOrderInfo,
    session: AsyncSession,

):
    stmt_customer_infol = (
        insert(OrderInfo).
        values(**data.dict())
    )
    await session.execute(stmt_customer_infol)
    await session.commit()
    return {"status": "Order created successfully"}


async def update_order_status(
    order_id: int,
    order_status: int,
    session: AsyncSession,

):
    stmt = (
        update(Order).
        values(order_status=order_status).
        where(Order.id == order_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Order created successfully"}


async def get_order(
    order_id: int,
    session: AsyncSession,

) -> Optional[GetOrder]:
    query = (
        select(Order).
        where(Order.id == order_id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response.total_price


async def get_order_info(
    order_id: int,
    session: AsyncSession,
):
    query = (
        select(OrderInfo).
        where(OrderInfo.order_id == order_id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response


# async def get_order_detail(
#     order_id: int,
#     session: AsyncSession,

# ) -> Optional[CreateOrderInfo]:
#     query = (
#         select(OrderInfo).
#         where(OrderInfo.id == order_id)
#     )
#     result = await session.execute(query)
#     response = result.scalar()
#     return response


async def get_order_detail(
    order_id: int,
    session: AsyncSession
):
    query = (
        select(
            Product.id,
            Category.name,
            Product.name,
            OrderDetail.quantity,
            OrderDetail.unit_price,
        )
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .join(Category, Category.id == Product.category_id)
        .where(OrderDetail.order_id == order_id)
    )
    result = await session.execute(query)
    # response = result.scalars().all()
    cart_items = []
    for row in result:
        row.name
        cart_item = CartItem(
            product_id=row[0],
            category_name=row[1],
            name=row[2],
            quantity=row[3],
            unit_price=row[4],
        )
        cart_items.append(cart_item)

    return cart_items


async def get_order_detail_test(
    order_id: int,
    session: AsyncSession
) -> List[OrderDetailTest]:
    query = (
        select(
            Category.name,
            Product.name,
            OrderDetail.quantity,
            OrderDetail.unit_price,
        )
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .join(Category, Category.id == Product.category_id)
        .where(OrderDetail.order_id == order_id)
    )
    result = await session.execute(query)
    return result.all()
