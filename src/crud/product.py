from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from ..models import Product
from ..schemas import ReadProduct


async def crud_get_all_products(
    category_id: int,
    session: AsyncSession,
    filter: Optional[bool] = None,
) -> List[ReadProduct]:
    query = (
        select(Product).
        where(
            Product.deleted_flag is not True,
            Product.category_id == category_id,
        ).
        order_by(
            Product.id.desc()
        )
    )
    if filter:
        query = query.where(Product.availability)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


async def crud_change_avail_roducts(
    product_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Product)
        .where(
            Product.id == product_id,
        )
        .values(availability=~Product.availability)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для availability изменен"}


async def crud_get_stop_list(
    session: AsyncSession
) -> List[ReadProduct]:
    query = (
        select(Product).
        where(
            Product.availability.is_(False)
        ).
        order_by(
            Product.id.desc(),
            Product.category_id
        )
    )
    result = await session.execute(query)
    products = result.scalars().all()
    return products


async def get_one_product(
    product_id: int,
    session: AsyncSession
):
    query = (
        select(Product).
        where(Product.deleted_flag is not True).
        where(Product.id == product_id)
    )
    result = await session.execute(query)
    products = result.scalar()
    return products


async def get_one_product_test(
    product_id: int,
    session: AsyncSession
):
    query = (
        select(Product.availability).
        where(Product.id == product_id)
    )
    result = await session.execute(query)
    products = result.scalar()
    return products
