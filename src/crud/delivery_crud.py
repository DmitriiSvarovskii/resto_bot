from datetime import datetime
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Delivery, OrderInfo
from src.schemas import delivery_schemas


async def crud_create_new_district(
    data: delivery_schemas.CreateDelivery,
    session: AsyncSession
):
    stmt = (
        insert(Delivery).
        values(**data.model_dump())
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, }


async def crud_read_delivery_districts(session: AsyncSession):
    query = (
        select(Delivery).
        order_by(Delivery.price.asc())
    )
    result = await session.execute(query)
    delivery_districts = result.scalars().all()
    return delivery_districts


async def crud_read_delivery_one_district(
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


async def crud_update_district(
    delivery_id: int,
    update_values: dict,
    session: AsyncSession
):
    stmt = (
        update(Delivery)
        .where(Delivery.id == delivery_id)
        .values(**update_values)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


async def crud_change_delete_flag_district(
    delivery_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Delivery).
        where(Delivery.id == delivery_id).
        values(
            deleted_flag=~Delivery.deleted_flag,
            deleted_at=datetime.now()
        )
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для deleted_flag изменен"}
