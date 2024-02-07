
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.schemas import ReadCustomerInfo, CustomerBase, CustomerCreate
from src.models import Customer


# async def add_tg_user(
#         data: CustomerCreate,
#         session: AsyncSession
# ):
#     query = (
#         select(Customer).
#         filter(
#             Customer.user_id == data.user_id
#         )
#     )
#     result = await session.execute(query)
#     customer = result.scalar()
#     if customer:
#         if not compare_customer_data(customer, data):
#             update_data = data.dict(exclude_unset=True)
#             await session.execute(
#                 update(Customer).
#                 where(
#                     Customer.user_id == data.user_id
#                 ).
#                 values(**update_data)
#             )
#             await session.commit()
#             return customer.admin
#         return customer.admin
#     else:
#         stmt = (
#             insert(Customer).
#             values(**data.dict())
#         )
#         await session.execute(stmt)
#         await session.commit()
#         return {"status": 201}


# async def crud_create_user(
#         data: CustomerCreate,
#         session: AsyncSession
# ):
#     query = (
#         select(Customer).
#         filter(
#             Customer.user_id == data.user_id
#         )
#     )
#     result = await session.execute(query)
#     customer = result.scalar()
#     if customer:
#         if not compare_customer_data(customer, data):
#             update_data = data.dict(exclude_unset=True)
#             await session.execute(
#                 update(Customer).
#                 where(
#                     Customer.user_id == data.user_id
#                 ).
#                 values(**update_data)
#             )
#             await session.commit()
#             return customer.admin
#         return customer.admin
#     else:
#         stmt = (
#             insert(Customer).
#             values(**data.dict())
#         )
#         await session.execute(stmt)
#         await session.commit()
#         return {"status": 201}


async def get_user(
    user_id: int,
    session: AsyncSession,

) -> Optional[ReadCustomerInfo]:
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
    resourse: Optional[str] = None,

) -> [CustomerBase]:
    query = select(Customer)
    if user_id:
        query = query.where(
            Customer.user_id == user_id,
        )
        result = await session.execute(query)
        response = result.scalar()
        return response
    if resourse:
        query = query.where(
            Customer.resourse == resourse,
        )
        result = await session.execute(query)
        response = result.fetchall()
        return response


async def get_customer_by_user_id(
    user_id: int,
    session: AsyncSession,
) -> Optional[CustomerBase]:
    query = (
        select(Customer)
        .filter(Customer.user_id == user_id)
    )
    result = await session.execute(query)
    customer = result.scalar()
    return customer


async def crud_create_customer(
    data: CustomerCreate,
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
    data: CustomerCreate,
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
