from src.database import get_async_session
from src.crud import crud_get_all_products
from src.keyboards import create_keyboard_product
from src.crud import (
    read_delivery_districts,
    decrease_cart_item,
    get_one_product,
    delete_cart_item,
)
from src.lexicons import LEXICON_RU
from src.schemas import CartCreate


async def get_delivery_districts():
    async for session in get_async_session():
        delivery_districts = await read_delivery_districts(
            session=session
        )
        break
    return delivery_districts
