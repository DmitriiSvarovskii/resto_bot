from src.crud import product_crud
from src.database import get_async_session


async def get_products_by_category(category_id):
    async for session in get_async_session():
        products = await product_crud.crud_get_all_products(
            category_id=category_id,
            filter=True,
            session=session
        )
        break
    return products


async def get_products_by_category_admin(category_id):
    async for session in get_async_session():
        products = await product_crud.crud_get_all_products(
            category_id=category_id,
            session=session
        )
        break
    return products


async def change_avail_roducts(product_id):
    async for session in get_async_session():
        await product_crud.crud_change_avail_roducts(
            product_id=product_id,
            session=session
        )
        break
    return {'status': 'ok'}
