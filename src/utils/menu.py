from src.database import get_async_session
from ..crud import get_user


async def get_user_info(user_id: int,):
    async for session in get_async_session():
        response = await get_user(
            user_id=user_id,
            session=session
        )
        break
    return response
