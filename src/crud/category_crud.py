from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category
from src.schemas import category_schemas


async def crud_get_all_categories(
    store_id: int,
    session: AsyncSession,
    filter: Optional[bool] = None
) -> List[category_schemas.GetCategory]:
    query = (
        select(Category).
        where(Category.deleted_flag.is_(False)).
        where(Category.store_id == store_id).
        order_by(Category.id.desc())
    )
    if filter:
        query = query.where(Category.availability)
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories


async def crud_get_one_category(
    category_id: int,
    store_id: int,
    session: AsyncSession,
) -> Optional[category_schemas.GetCategory]:
    query = (
        select(Category)
        .where(
            Category.id == category_id,
            Category.store_id == store_id
        )
    )
    result = await session.execute(query)
    category = result.scalar()
    return category


async def crud_change_avail_categories(
    category_id: int,
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Category)
        .where(
            Category.id == category_id,
            Category.store_id == store_id
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


async def crud_update_category_name(
    category_id: int,
    store_id: int,
    category_name_rus: str,
    category_name_en: str,
    session: AsyncSession
):

    stmt = (
        update(Category)
        .where(
            Category.id == category_id,
            Category.store_id == store_id
        )
        .values(name_rus=category_name_rus, name_en=category_name_en)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", }


async def crud_change_delete_flag_category(
    category_id: int,
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Category)
        .where(
            Category.id == category_id,
            Category.store_id == store_id
        )
        .values(
            deleted_flag=~Category.deleted_flag,
            deleted_at=datetime.now()
        )
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для deleted_flag изменен"}
