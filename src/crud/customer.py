from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.schemas import ReadCustomerInfo, CustomerBase
from src.models import Customer


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
