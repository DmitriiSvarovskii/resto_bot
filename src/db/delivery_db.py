from src.db.database import get_async_session
from src.crud import delivery_crud as del_crud


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


