from datetime import time
from src.db.database import get_async_session
from src.crud import store_crud


async def get_store_info():
    async for session in get_async_session():
        response = await store_crud.crud_get_store_info(session=session)
        return response


async def change_is_active_bot():
    async for session in get_async_session():
        await store_crud.crud_change_is_active_bot(
            session=session
        )
        return {'status': 'ok'}


async def db_update_opening_hours(
    opening_time: time,
    closing_time: time,
):
    async for session in get_async_session():
        await store_crud.crud_update_opening_hours(
            opening_time=opening_time,
            closing_time=closing_time,
            session=session
        )
        return {'status': 'ok'}
