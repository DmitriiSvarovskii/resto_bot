from src.db.database import get_async_session
from src.crud import delivery_crud as del_crud
from src.schemas import delivery_schemas


async def get_delivery_one_district(delivery_id: int):
    async for session in get_async_session():
        response = await del_crud.crud_read_delivery_one_district(
            delivery_id=delivery_id,
            session=session
        )
        return response


async def get_delivery_districts():
    async for session in get_async_session():
        delivery_districts = await del_crud.crud_read_delivery_districts(
            session=session
        )
        break
    return delivery_districts


async def db_update_district(
    delivery_id: int,
    update_values: dict,
):
    async for session in get_async_session():
        await del_crud.crud_update_district(
            delivery_id=delivery_id,
            update_values=update_values,
            session=session
        )
        return {'status': 'ok'}


async def db_create_new_district(data: delivery_schemas.CreateDelivery):
    async for session in get_async_session():
        await del_crud.crud_create_new_district(
            data=data,
            session=session
        )
        break
    return {'status': 'ok'}


async def db_change_delete_flag_district(
    delivery_id: int
):
    async for session in get_async_session():
        await del_crud.crud_change_delete_flag_district(
            delivery_id=delivery_id,
            session=session
        )
        break
    return {'status': 'ok'}
