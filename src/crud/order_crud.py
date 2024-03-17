from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.schemas import order_schemas, cart_schemas
from src.models import (
    Category,
    Product,
    Order,
    OrderDetail,
    OrderInfo
)


async def crud_create_orders(
    data_order: order_schemas.CreateOrder,
    session: AsyncSession,
):
    stmt_order = (
        insert(Order).
        values(**data_order.model_dump()).
        returning(Order.id)
    )
    result = await session.execute(stmt_order)
    await session.commit()
    return result.scalar()


async def crud_create_new_order_details(
    data: List[order_schemas.CreateOrderDetail],
    session: AsyncSession,
):
    stmt = (
        insert(OrderDetail).
        values(data)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Order created successfully"}


async def crud_create_order_info(
    data: order_schemas.CreateOrderInfo,
    session: AsyncSession,

):
    stmt_customer_infol = (
        insert(OrderInfo).
        values(**data.model_dump())
    )
    await session.execute(stmt_customer_infol)
    await session.commit()
    return {"status": "Order created successfully"}


async def crud_update_order_status(
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


async def crud_get_order(
    order_id: int,
    session: AsyncSession,

) -> Optional[order_schemas.ReadOrder]:
    query = (
        select(Order).
        where(Order.id == order_id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response


async def crud_get_order_list(
    user_id: int,
    session: AsyncSession,

) -> List[order_schemas.ReadOrder]:
    query = (
        select(Order)
        .where(Order.user_id == user_id)
        .limit(5)
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response


async def crud_get_order_info(
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


async def crud_get_order_detail(
    order_id: int,
    session: AsyncSession
) -> List[cart_schemas.CartItem]:
    query = (
        select(
            Product.id.label("product_id"),
            Category.name.label("category_name"),
            Product.name.label("name"),
            OrderDetail.quantity.label("quantity"),
            OrderDetail.unit_price.label("unit_price"),
        )
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .join(Category, Category.id == Product.category_id)
        .where(OrderDetail.order_id == order_id)
    )
    result = await session.execute(query)
    return [cart_schemas.CartItem(**row._asdict()) for row in result]


async def crud_get_order_detail_report(
    order_id: int,
    session: AsyncSession
) -> List[order_schemas.ReadOrderDetail]:
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


async def crud_get_pending_orders_list(
        session: AsyncSession,
) -> List[order_schemas.ReadOrderList]:
    query = (
        select(Order)
        .where(Order.order_status != "Выполнен",
               Order.order_status != "Отменён")
        .order_by(Order.id)
    )

    result = await session.execute(query)
    return result.scalars().all()
