import asyncio
from src.db.cart_db import get_total_price_cart2


async def main():
    user_id = 606825877
    result = await get_total_price_cart2(user_id)
    print(result)
asyncio.run(main())
