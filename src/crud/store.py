from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
# from src.database import get_async_session
from src.models import Store
from src.schemas import GetStore
from typing import List, Optional


async def crud_get_store_info(session: AsyncSession) -> Optional[GetStore]:
    query = (
        select(Store)
    )
    result = await session.execute(query)
    store = result.scalar()
    return store


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
