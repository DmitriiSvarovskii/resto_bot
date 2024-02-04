from aiogram.types import CallbackQuery

from ..callbacks import ProductIdCallbackFactory
from src.database import get_async_session
from ..lexicons import LEXICON_RU
from ..schemas import CartCreate
from ..crud import (
    crud_get_all_products,
    crud_change_avail_roducts,
    crud_change_avail_categories,
)
from ..keyboards import (
    create_keyboard_product,
    create_keyboard_product_admin,
)
from ..crud import (
    add_to_cart,
    decrease_cart_item,
    get_one_product,
    delete_cart_item,
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
    keyboard = await create_keyboard_product_admin(
        products=products
    )
    return keyboard


async def process_cart_action(
    callback: CallbackQuery,
    callback_data: ProductIdCallbackFactory,
):
    product_id = callback_data.product_id
    user_id = callback.message.chat.id

    cart_data = CartCreate(
        product_id=product_id,
        user_id=user_id
    )

    type_pr = callback_data.type_pr

    async for session in get_async_session():
        if type_pr == 'plus':
            response = await add_to_cart(
                data=cart_data,
                session=session
            )
            await callback.answer(text=response['message'])

        elif type_pr == 'minus':
            response = await decrease_cart_item(
                data=cart_data,
                session=session
            )
            if response['message'] == LEXICON_RU['cart_error']:
                await callback.answer(
                    text=response['message'],
                    show_alert=True
                )
                break
            await callback.answer(text=response['message'])

        elif type_pr == 'compound':
            compound_text = await get_one_product(
                product_id=cart_data.product_id,
                session=session
            )
            await callback.answer(
                text=compound_text.description,
                show_alert=True
            )
        elif type_pr == 'del':
            await delete_cart_item(
                data=cart_data,
                session=session,
            )

            await callback.answer(text='message')

            # if not cart_data:
            #     await callback.message.answer(LEXICON_RU['cart_error'])

            # else:
            #     await delete_cart_item(
            #         data=cart_data,
            #         session=session,
            #     )
        break
