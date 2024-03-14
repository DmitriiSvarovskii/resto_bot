from src.crud import product_crud
from src.db.database import get_async_session
from src.schemas import product_schemas


async def get_products_by_category(category_id: int):
    async for session in get_async_session():
        products = await product_crud.crud_get_all_products(
            category_id=category_id,
            filter=True,
            session=session
        )
        break
    return products


async def get_products_by_category_admin(category_id: int):
    async for session in get_async_session():
        products = await product_crud.crud_get_all_products(
            category_id=category_id,
            session=session
        )
        break
    return products


async def change_avail_roducts(product_id: int):
    async for session in get_async_session():
        await product_crud.crud_change_avail_roducts(
            product_id=product_id,
            session=session
        )
        break
    return {'status': 'ok'}


async def db_create_new_product(data: product_schemas.CreateProduct):
    async for session in get_async_session():
        await product_crud.crud_create_new_product(
            data=data,
            session=session
        )
        break
    return {'status': 'ok'}
