from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
# from src.database import get_async_session
from src.models import Delivery
# from .schemas import CategoryCreate, CategoryUpdate
# from typing import List


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
