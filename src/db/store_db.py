from datetime import time
from src.db.database import get_async_session
from src.crud import store_crud


async def get_store_info(store_id: int):
    async for session in get_async_session():
        response = await store_crud.crud_get_store_info(
            store_id=store_id,
            session=session
        )
        return response


async def db_get_store_list():
    async for session in get_async_session():
        response = await store_crud.crud_get_store_list(session=session)
        return response


async def change_is_active_bot(store_id: int):
    async for session in get_async_session():
        await store_crud.crud_change_is_active_bot(
            store_id=store_id,
            session=session
        )
        return {'status': 'ok'}


async def db_update_opening_hours(
    store_id: int,
    opening_time: time,
    closing_time: time,
):
    async for session in get_async_session():
        await store_crud.crud_update_opening_hours(
            store_id=store_id,
            opening_time=opening_time,
            closing_time=closing_time,
            session=session
        )
        return {'status': 'ok'}


async def db_update_store(
    store_id: int,
    update_values: dict,
):
    async for session in get_async_session():
        await store_crud.crud_update_store(
            store_id=store_id,
            update_values=update_values,
            session=session
        )
        return {'status': 'ok'}
