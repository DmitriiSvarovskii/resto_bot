from datetime import time
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.models import Store
from src.schemas import store_schemas


async def crud_get_store_info(
    store_id: int,
    session: AsyncSession
) -> Optional[store_schemas.GetStore]:
    query = (
        select(Store)
        .where(Store.id == store_id)
    )
    result = await session.execute(query)
    scalar_result = result.scalar()
    return scalar_result


async def crud_get_store_list(
    session: AsyncSession
) -> List[store_schemas.GetStore]:
    query = (
        select(Store)
        .order_by(Store.id.asc())
    )
    result = await session.execute(query)
    scalar_result = result.scalars().all()
    return scalar_result


async def crud_change_is_active_bot(
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Store)
        .where(Store.id == store_id)
        .values(is_active=~Store.is_active)
    )

    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для is_active изменен"}


async def crud_update_opening_hours(
    opening_time: time,
    closing_time: time,
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Store)
        .where(Store.id == store_id)
        .values(
            opening_time=opening_time,
            closing_time=closing_time
        )
    )

    await session.execute(stmt)
    await session.commit()
    return {"message": "success"}


async def crud_update_store(
    store_id: int,
    update_values: dict,
    session: AsyncSession
):
    stmt = (
        update(Store)
        .where(Store.id == store_id)
        .values(**update_values)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
