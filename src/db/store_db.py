from src.database import get_async_session
from src.crud import store_crud


async def get_store_info():
    async for session in get_async_session():
        response = await store_crud.crud_get_store_info(session=session)
        break
    return response
