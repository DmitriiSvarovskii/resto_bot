from src.db.database import get_async_session
from src.crud import cart_crud, product_crud
from src.schemas import cart_schemas


async def get_cart_items_and_totals(
    user_id: int,
):
    async for session in get_async_session():
        response = await cart_crud.crud_read_cart_items_and_totals(
            user_id=user_id,
            session=session
        )
        break
    return response


async def get_total_price_cart(
    user_id: int,
):
    async for session in get_async_session():
        response = await cart_crud.crud_total_price_cart_by_id(
            user_id=user_id,
            session=session
        )
        break
    return response if response is not None else 0


async def delete_cart_items_by_user_id(
    user_id: int,
):
    async for session in get_async_session():
        await cart_crud.crud_delete_cart_items_by_user_id(
            user_id=user_id,
            session=session
        )
        break


async def add_to_cart(data: cart_schemas.CartCreate):
    async for session in get_async_session():
        response = await cart_crud.crud_add_to_cart(
            data=data,
            session=session
        )
        break
    return response


async def decrease_cart_item(data: cart_schemas.CartCreate):
    async for session in get_async_session():
        response = await cart_crud.crud_decrease_cart_item(
            data=data,
            session=session
        )
        break
    return response


async def get_one_product(product_id: int):
    async for session in get_async_session():
        compound_text = await product_crud.crud_get_one_product(
            product_id=product_id,
            session=session
        )
        break
    return compound_text


async def delete_cart_item(data: cart_schemas.CartCreate):
    async for session in get_async_session():
        await cart_crud.crud_delete_cart_item(
            data=data,
            session=session,
        )
        break
