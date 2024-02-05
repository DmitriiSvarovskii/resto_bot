from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message

from src.database import get_async_session
from src.models import Customer
from src.schemas import CustomerCreate
from src.keyboards import create_keyboard_main
from src.lexicons import LEXICON_RU


async def process_start_command(message: Message):
    async for session in get_async_session():
        if message.text.strip() == "/start":
            resourse = None
        else:
            resourse = message.text.replace("/start", "").strip()
        new_customer_data = (
            CustomerCreate(
                user_id=message.from_user.id,
                resourse=resourse,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
            )
        )
        await add_tg_user(
            data=new_customer_data,
            session=session
        )
        break

    keyboard = await create_keyboard_main(message.chat.id)

    await message.answer(
        text=LEXICON_RU['start'],
        reply_markup=keyboard
    )


async def add_tg_user(
        data: CustomerCreate,
        session: AsyncSession
):
    query = (
        select(Customer).
        filter(
            Customer.user_id == data.user_id
        )
    )
    result = await session.execute(query)
    customer = result.scalar()
    if customer:
        if not compare_customer_data(customer, data):
            update_data = data.dict(exclude_unset=True)
            await session.execute(
                update(Customer).
                where(
                    Customer.user_id == data.user_id
                ).
                values(**update_data)
            )
            await session.commit()
            return customer.admin
        return customer.admin
    else:
        stmt = (
            insert(Customer).
            values(**data.dict())
        )
        await session.execute(stmt)
        await session.commit()
        return {"status": 201}


def compare_customer_data(
    customer: Customer,
    data: CustomerCreate
) -> bool:
    if customer is None:
        return False
    if customer.first_name != data.first_name:
        return False
    if customer.last_name != data.last_name:
        return False
    if customer.username != data.username:
        return False
    if customer.resourse != data.resourse:
        return False
    return True
