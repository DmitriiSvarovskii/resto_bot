from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Delivery, OrderInfo


async def read_delivery_districts(session: AsyncSession):
    query = (
        select(Delivery).
        order_by(Delivery.id.desc())
    )
    result = await session.execute(query)
    delivery_districts = result.scalars().all()
    return delivery_districts


async def read_delivery_one_district(
    delivery_id: int,
    session: AsyncSession
):
    query = (
        select(Delivery).
        where(Delivery.id == delivery_id)
    )
    result = await session.execute(query)
    delivery_district = result.scalar()

    return delivery_district


async def get_delivery_time_by_order_id(
    order_id: int,
    session: AsyncSession
):
    query = (
        select(Delivery.delivery_time)
        .join(OrderInfo, OrderInfo.delivery_id == Delivery.id)
        .where(OrderInfo.order_id == order_id)
    )
    result = await session.execute(query)
    delivery_time = result.scalar()
    return delivery_time
