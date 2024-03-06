from src.db.database import get_async_session
from src.crud import category_crud as cat_crud
from src.schemas import category_schemas


async def get_all_categories():
    async for session in get_async_session():
        categories = await cat_crud.crud_get_all_categories(
            filter=True,
            session=session
        )
        return categories


async def create_new_category(data: category_schemas.CreateCategory):
    async for session in get_async_session():
        categories = await cat_crud.crud_create_category(
            data=data,
            session=session
        )
        return categories


async def get_all_categories_admin():
    async for session in get_async_session():
        categories = await cat_crud.crud_get_all_categories(
            session=session
        )
        return categories


async def change_avail_category(category_id):
    async for session in get_async_session():
        await cat_crud.crud_change_avail_categories(
            category_id=category_id,
            session=session
        )
        break
    return {'status': 'ok'}
