from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.models import Category
from src.schemas import category_schemas


async def crud_get_all_categories(
    session: AsyncSession,
    filter: Optional[bool] = None
) -> List[category_schemas.GetCategory]:
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


async def crud_create_category(
    data: category_schemas.CreateCategory,
    session: AsyncSession,
):
    stmt = (
        insert(Category)
        .values(**data.model_dump())
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Создана новая категория"}
