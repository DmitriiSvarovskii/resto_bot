from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.models import Category
from src.schemas import GetCategory


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
