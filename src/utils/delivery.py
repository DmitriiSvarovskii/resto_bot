from ..database import get_async_session
from ..crud import read_delivery_districts


async def get_delivery_districts():
    async for session in get_async_session():
        delivery_districts = await read_delivery_districts(
            session=session
        )
        break
    return delivery_districts
