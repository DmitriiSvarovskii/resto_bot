from src.db.database import get_async_session
from src.schemas import customer_schemas
from src.crud import customer_crud as cust_crud
from src.utils import customer_utils as cust_utils


async def add_new_user_to_database(
    customer_data: customer_schemas.CustomerCreate
):
    async for session in get_async_session():
        await cust_utils.add_tg_user(
            data=customer_data,
            session=session
        )
        break


async def get_user_info_by_id(
    user_id: int
):
    async for session in get_async_session():
        response = await cust_crud.get_customer_by_user_id(
            user_id=user_id,
            session=session
        )
        break
    return response


async def db_get_users_list():
    async for session in get_async_session():
        response = await cust_crud.crud_get_users_list(
            session=session
        )
        break
    return response
