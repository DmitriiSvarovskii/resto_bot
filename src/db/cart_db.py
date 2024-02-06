from src.database import get_async_session
from src.crud import cart


async def get_total_price_cart(
    user_id: int,
):
    async for session in get_async_session():
        response = await cart.read_cart_items_and_totals(
            user_id=user_id,
            session=session
        )
        break
    return response
