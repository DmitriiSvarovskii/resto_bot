from src.crud import crud_get_all_products
from src.database import get_async_session


async def get_products_by_category_admin(category_id):
    async for session in get_async_session():
        products = await crud_get_all_products(
            category_id=category_id,
            session=session
        )
        break
    return products
