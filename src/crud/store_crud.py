from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.models import Store
from src.schemas import store_schemas


async def crud_get_store_info(
    session: AsyncSession
) -> Optional[store_schemas.GetStore]:
    query = (
        select(Store)
    )
    result = await session.execute(query)
    scalar_result = result.scalar()
    return scalar_result


async def crud_change_is_active_bot(
    session: AsyncSession,
):
    stmt = (
        update(Store)
        .values(is_active=~Store.is_active)
    )

    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для is_active изменен"}
