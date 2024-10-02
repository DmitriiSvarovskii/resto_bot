from datetime import datetime
from typing import List, Optional, Any

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product, Category
from src.schemas import product_schemas


import logging

logger = logging.getLogger(__name__)


async def crud_get_all_products(
    store_id: int,
    category_id: int,
    session: AsyncSession,
    filter: Optional[bool] = None,
) -> List[product_schemas.ReadProduct]:
    query = (
        select(Product).
        where(
            Product.deleted_flag.is_(False),
            Product.category_id == category_id,
            Product.store_id == store_id
        ).
        order_by(Product.id.asc())
    )
    if filter:
        query = query.where(Product.availability)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


# async def crud_get_all_popular_products(
#     store_id: int,
#     session: AsyncSession,
#     filter: Optional[bool] = None,
# ) -> List[product_schemas.ReadProduct]:
#     query = (
#         select(Product).
#         where(
#             Product.deleted_flag.is_(False),
#             Product.popular,
#             Product.store_id == store_id
#         ).
#         order_by(Product.id.asc())
#     )
#     if filter:
#         query = query.where(Product.availability)
#     result = await session.execute(query)
#     products = result.scalars().all()
#     return products

async def crud_get_all_popular_products(
    store_id: int,
    session: AsyncSession,
    filter: Optional[bool] = None,
) -> List[product_schemas.ReadProduct]:
    """
    Получает все популярные продукты для заданного магазина,
    фильтруя по доступности категории, если указано.

    :param store_id: ID магазина
    :param session: Асинхронная сессия SQLAlchemy
    :param filter: Флаг для фильтрации по доступности продукта
    :return: Список популярных продуктов
    """
    try:
        logger.info(
            f"Fetching popular products for store_id={store_id} with filter={filter}")

        # Создаём базовый запрос с JOIN на Category
        query = (
            select(Product)
            .join(Category, Product.category_id == Category.id)
            .where(
                Product.deleted_flag.is_(False),
                Product.popular.is_(True),
                Product.store_id == store_id,
                # Фильтр по доступности категории
                Category.availability.is_(True)
            )
            .order_by(Product.id.asc())
        )

        # Дополнительный фильтр по доступности продукта, если указан
        if filter:
            query = query.where(Product.availability.is_(True))
            logger.debug(
                "Applied additional filter: Product.availability == True")

        logger.debug(f"Constructed query: {query}")

        # Выполнение запроса
        result = await session.execute(query)
        products = result.scalars().all()

        logger.info(
            f"Fetched {len(products)} popular products for store_id={store_id}")

        return products

    except Exception as e:
        logger.exception(f"Error fetching popular products: {e}")
        return []


async def crud_change_avail_roducts(
    product_id: int,
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Product)
        .where(Product.id == product_id,
               Product.store_id == store_id)
        .values(availability=~Product.availability)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для availability изменен"}


async def crud_change_popular_roducts(
    product_id: int,
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Product)
        .where(Product.id == product_id,
               Product.store_id == store_id)
        .values(popular=~Product.popular)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для popular изменен"}


async def crud_get_stop_list(
    store_id: int,
    session: AsyncSession
) -> List[product_schemas.ReadProduct]:
    query = (
        select(Product).
        where(Product.availability.is_(False),
              Product.store_id == store_id).
        order_by(
            Product.id.asc(),
            Product.category_id
        )
    )
    result = await session.execute(query)
    products = result.scalars().all()
    return products


async def crud_get_one_product(
    product_id: int,
    store_id: int,
    session: AsyncSession
) -> Optional[product_schemas.ReadProduct]:
    query = (
        select(Product).
        where(
            Product.deleted_flag.is_(False),
            Product.id == product_id,
            Product.store_id == store_id
        )
    )
    result = await session.execute(query)
    products = result.scalar()
    return products


async def crud_create_new_product(
    data: product_schemas.CreateProduct,
    session: AsyncSession
):
    stmt = (
        insert(Product).
        values(**data.model_dump())
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, }


async def crud_update_product(
    product_id: int,
    store_id: int,
    data: dict,
    session: AsyncSession
):
    # update_data = {field_name: new_value}
    stmt = (
        update(Product).
        where(Product.id == product_id,
              Product.store_id == store_id).
        values(**{key: value for key, value in data.items() if key != 'product_id'})
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", }


async def crud_change_delete_flag_product(
    product_id: int,
    store_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Product).
        where(Product.id == product_id,
              Product.store_id == store_id).
        values(
            deleted_flag=~Product.deleted_flag,
            deleted_at=datetime.now()
        )
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Статус для deleted_flag изменен"}
