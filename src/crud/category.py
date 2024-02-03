from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession
# from src.database import get_async_session
from src.models import Category
from src.schemas import GetCategory
from typing import List, Optional


async def crud_get_all_categories(
    session: AsyncSession,
    filter: Optional[bool] = None
) -> List[GetCategory]:
    query = (
        select(Category).
        where(
            Category.deleted_flag is not True
        ).
        order_by(Category.id.desc())
    )
    if filter:
        query = query.where(Category.availability)
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories


async def crud_change_avail_categories(
    category_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Category)
        .where(
            Category.id == category_id,
        )
        .values(availability=~Category.availability)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для availability изменен"}