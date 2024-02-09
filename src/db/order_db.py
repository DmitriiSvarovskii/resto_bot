from typing import Optional, List

from src.crud import delivery_crud, order_crud
from src.services import ORDER_TYPES
from src.database import get_async_session
from src.schemas import order_schemas
from src.schemas import CartItem


async def get_order_list(
    user_id: int,
):
    async for session in get_async_session():
        response = await order_crud.crud_get_order_list(
            user_id=user_id,
            session=session
        )
        return response


async def get_delivery_time(
    order_id: int,
):
    async for session in get_async_session():
        response = await delivery_crud.get_delivery_time_by_order_id(
            order_id=order_id,
            session=session
        )
        return response


async def create_orders(
    data_order: order_schemas.CreateOrder,
):
    async for session in get_async_session():
        response = await order_crud.crud_create_orders(
            data_order=data_order,
            session=session
        )
        return response


async def create_new_order_details(
    data: order_schemas.CreateOrderDetails,
):
    async for session in get_async_session():
        await order_crud.crud_create_new_order_details(
            data=data,
            session=session
        )
        break


async def create_order_info(
    data: order_schemas.CreateOrderInfo,
):
    async for session in get_async_session():
        await order_crud.crud_create_order_info(
            data=data,
            session=session
        )
        break


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
            response = await delivery_crud.get_delivery_time_by_order_id(
                order_id=order_id,
                session=session
            )
            return response
        break
    return None


async def get_order(
    order_id: int,
):
    async for session in get_async_session():
        response = await order_crud.crud_get_order(
            order_id=order_id,
            session=session
        )
        return response


async def get_order_info(
    order_id: int,
):
    async for session in get_async_session():
        response = await order_crud.crud_get_order_info(
            order_id=order_id,
            session=session
        )
        return response


async def get_order_detail(
    order_id: int,
) -> List[CartItem]:
    async for session in get_async_session():
        response = await order_crud.crud_get_order_detail(
            order_id=order_id,
            session=session
        )
        return response


async def get_pending_orders_list() -> List[order_schemas.ReadOrderList]:
    async for session in get_async_session():
        response = await order_crud.crud_get_pending_orders_list(
            session=session
        )
        return response
