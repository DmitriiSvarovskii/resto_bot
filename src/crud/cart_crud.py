from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional

from src.models import Product, Cart, Category
from src.schemas import cart_schemas
from src.lexicons import LEXICON_RU


async def crud_read_cart_items_and_totals(
    user_id: int,
    session: AsyncSession
) -> Optional[cart_schemas.CartResponse]:
    query = (
        select(
            Product.id.label("product_id"),
            Category.name.label("category_name"),
            Product.name,
            Cart.quantity,
            (Cart.quantity * Product.price).label("unit_price"),
            (Cart.quantity * Product.price_box).label("box_price"),
        )
        .join(Cart, Cart.product_id == Product.id)
        .join(Category, Category.id == Product.category_id)
        .where(
            Cart.user_id == user_id,
            Cart.quantity > 0
        )
        .group_by(Category.id, Product.id, Cart.quantity,
                  Product.name, Cart.user_id)
    )
    result = await session.execute(query)

    cart_items = [cart_schemas.CartItem(**item._asdict()) for item in result]
    total_price = sum(cart_item.unit_price for cart_item in cart_items)

    response_data = cart_schemas.CartResponse(
        cart_items=cart_items,
        total_price=total_price
    )

    return response_data


async def crud_total_price_cart_by_id(
    user_id: int,
    session: AsyncSession
) -> Optional[cart_schemas.CartItemTotal]:
    query = (
        select(
            func.sum(Cart.quantity * Product.price).label("total_price")
        )
        .join(Product, Cart.product_id == Product.id)
        .join(Category, Category.id == Product.category_id)
        .where(Cart.user_id == user_id)
    )
    result = await session.execute(query)
    scalar_result = result.scalar_one()
    return scalar_result


async def crud_add_to_cart(
    data: cart_schemas.CartCreate,
    session: AsyncSession
):
    query = (
        select(Cart).
        where(
            Cart.user_id == data.user_id,
            Cart.product_id == data.product_id
        )
    )
    result = await session.execute(query)
    cart_item = result.scalars().all()

    if cart_item:
        stmt = (
            update(Cart).
            where(
                Cart.user_id == data.user_id,
                Cart.product_id == data.product_id
            ).
            values(quantity=func.coalesce(Cart.quantity, 0) + 1)
        )
        await session.execute(stmt)
    else:
        stmt = (
            insert(Cart).
            values(**data.model_dump(), quantity=1)
        )
        await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'message': 'Добавил!'}


async def crud_decrease_cart_item(
    data: cart_schemas.CartCreate,
    session: AsyncSession
):
    query = (
        select(Cart).
        where(
            Cart.user_id == data.user_id,
            Cart.product_id == data.product_id
        )
    )
    result = await session.execute(query)
    cart_item = result.scalar()

    if cart_item:
        if cart_item.quantity:
            await update_cart_item_quantity(data, session)
        else:
            await crud_delete_cart_item(data, session)
    else:
        return {"message": LEXICON_RU['cart_error']}

    return {"status": 201, 'message': 'Удалил!'}


async def update_cart_item_quantity(
    data: cart_schemas.CartCreate,
    session: AsyncSession
):
    stmt = (
        update(Cart).
        where(
            Cart.user_id == data.user_id,
            Cart.product_id == data.product_id
        ).
        values(quantity=Cart.quantity - 1)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": 'ok'}


async def crud_delete_cart_item(
    data: cart_schemas.CartCreate,
    session: AsyncSession
):
    stmt = (
        delete(Cart).
        where(
            Cart.user_id == data.user_id,
            Cart.product_id == data.product_id
        )
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": 'ok'}


async def crud_delete_cart_items_by_user_id(
    user_id: int,
    session: Session
):
    stmt = (
        delete(Cart).
        where(Cart.user_id == user_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
