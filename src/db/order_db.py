from src.crud import crud_get_order_list, delivery
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
