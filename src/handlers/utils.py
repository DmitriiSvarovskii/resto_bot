from aiogram.types import CallbackQuery

from src.callbacks import ProductIdCallbackFactory
from src.database import get_async_session
from src.db import cart_db
from src.lexicons import LEXICON_RU
from src.crud import (
    crud_get_all_products,
    crud_change_avail_roducts,
    crud_change_avail_categories,
)
from src.keyboards import product_keyboards
from src.keyboards import (
    create_keyboard_product,
    # create_keyboard_product_admin,
)
from src.crud import (
    # add_to_cart,
    # decrease_cart_item,
    # get_one_product,
    # delete_cart_item,
    crud_change_is_active_bot,
)


async def get_products_by_category(category_id):
    async for session in get_async_session():
        products = await crud_get_all_products(
            category_id=category_id,
            filter=True,
            session=session
        )
        break
    return products


async def change_avail_roducts(product_id):
    async for session in get_async_session():
        await crud_change_avail_roducts(
            product_id=product_id,
            session=session
        )
        break
    return {'status': 'ok'}


async def change_is_active_bot():
    async for session in get_async_session():
        await crud_change_is_active_bot(
            session=session
        )
        break
    return {'status': 'ok'}


async def change_avail_category(category_id):
    async for session in get_async_session():
        await crud_change_avail_categories(
            category_id=category_id,
            session=session
        )
        break
    return {'status': 'ok'}


async def get_keyboard_products_by_category(products, user_id):
    async for session in get_async_session():
        if products:
            keyboard = await create_keyboard_product(
                products=products,
                user_id=user_id,
                session=session
            )
        break
    return keyboard


async def get_admin_keyboard_products_by_category(products):
    keyboard = await product_keyboards.create_keyboard_product_admin(
        products=products
    )
    return keyboard
