from aiogram.types import Message
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Customer
from src.schemas import CustomerCreate
from src.crud import customer_crud as cust


def compare_customer_data(
    customer: Customer,
    data: CustomerCreate
) -> bool:
    return (
        customer and
        customer.first_name == data.first_name and
        customer.last_name == data.last_name and
        customer.username == data.username and
        customer.resourse == data.resourse
    )


async def create_customer_data_from_message(
    message: Message
) -> Optional[CustomerCreate]:
    if message.text.strip() == "/start":
        resource = None
    else:
        resource = message.text.replace("/start", "").strip()

    customer_data = CustomerCreate(
        user_id=message.from_user.id,
        resourse=resource,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username
    )
    return customer_data


async def add_tg_user(
        data: CustomerCreate,
        session: AsyncSession
):
    try:
        customer = await cust.get_customer_by_user_id(
            user_id=data.user_id,
            session=session
        )

        if customer:
            if not compare_customer_data(customer, data):
                await cust.crud_update_customer(
                    data=data,
                    session=session
                )
            return customer
        else:
            created_customer = await cust.crud_create_customer(
                data=data,
                session=session
            )
            return created_customer
    except Exception:
        return None
