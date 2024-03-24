from typing import Optional, Union, List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import customer_schemas
from src.models import Customer


async def crud_get_users_list(
    session: AsyncSession,

) -> List[customer_schemas.ReadCustomerInfo]:
    query = (
        select(Customer)
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response


async def get_user(
    user_id: int,
    session: AsyncSession,

) -> Optional[customer_schemas.ReadCustomerInfo]:
    query = (
        select(Customer).
        where(Customer.user_id == user_id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response


async def get_user_info(
    session: AsyncSession,
    user_id: Optional[int] = None,
    resourse: Optional[str] = None
) -> Union[customer_schemas.CustomerBase, List[customer_schemas.CustomerBase]]:
    query = select(Customer)
    if user_id:
        query = query.where(Customer.user_id == user_id)
        result = await session.execute(query)
        response = result.scalar()
        return response
    if resourse:
        query = query.where(Customer.resourse == resourse)
        result = await session.execute(query)
        response = result.fetchall()
        return response


async def get_customer_by_user_id(
    user_id: int,
    session: AsyncSession,
) -> Optional[customer_schemas.CustomerBase]:
    query = (
        select(Customer)
        .filter(Customer.user_id == user_id)
    )
    result = await session.execute(query)
    customer = result.scalar()
    return customer


async def crud_create_customer(
    data: customer_schemas.CustomerCreate,
    session: AsyncSession,
):
    stmt = (
        insert(Customer).
        values(**data.model_dump())
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 201}


async def crud_update_customer(
    data: customer_schemas.CustomerCreate,
    session: AsyncSession,
):
    update_data = data.model_dump(exclude_unset=True)
    stmt = (
        update(Customer).
        where(Customer.user_id == data.user_id).
        values(**update_data)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 200}
