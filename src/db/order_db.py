from typing import Optional

from src.crud import crud_get_order_list, delivery, order_crud
from src.services import ORDER_TYPES
from src.database import get_async_session


async def get_order_list(
    user_id: int,
):
    async for session in get_async_session():
        response = await crud_get_order_list(
            user_id=user_id,
            session=session
        )
        break
    return response


async def get_delivery_time(
    order_id: int,
):
    async for session in get_async_session():
        response = await delivery.get_delivery_time_by_order_id(
            order_id=order_id,
            session=session
        )
        break
    return response


async def update_order_status(
    order_status: int,
    order_id: int,
    order_type: Optional[int] = None,
):
    async for session in get_async_session():
        await order_crud.crud_update_order_status(
            order_status=order_status,
            order_id=order_id,
            session=session
        )
        if (order_type is not None
            and
                order_type == ORDER_TYPES['delivery']['id']):
            response = await delivery.get_delivery_time_by_order_id(
                order_id=order_id,
                session=session
            )
            return response
        break
    return None
