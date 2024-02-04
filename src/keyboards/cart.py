from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..lexicons import LEXICON_KEYBOARDS_RU, LEXICON_RU
from ..callbacks import CartEditCallbackFactory, CreateOrderCallbackFactory
from ..crud import read_cart_items_and_totals
from src.database import get_async_session
from ..services import ORDER_TYPES, ORDER_STATUSES
from .main_keyboard import create_keyboard_main


def create_keyboard_cart(mess_id: int):
    button_main_menu: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['menu'],
        callback_data='press_menu')
    button_empty: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['clear'],
        callback_data='press_empty')
    button_free_delivery: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['free_delivery'],
        callback_data=CreateOrderCallbackFactory(
            order_type=ORDER_TYPES['takeaway']['id'],
            status=ORDER_STATUSES['new']['id'],
            mess_id=mess_id,
        ).pack())
    button_delivery_pay: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['delivery_pay'],
        callback_data='press_delivery_pay')
    button_edit: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['edit'],
        callback_data='press_edit_cart')
    button_comment: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_KEYBOARDS_RU['comment'],
        callback_data='press_comment')

    keyboard_cart_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_cart_builder.row(button_comment)

    keyboard_cart_builder.row(
        button_free_delivery,
        button_delivery_pay
    )
    keyboard_cart_builder.row(
        button_main_menu,
        button_empty,
        button_edit,
        width=3
    )

    return keyboard_cart_builder.as_markup()


async def create_keyboards_products_cart(callback, user_id):
    async for session in get_async_session():
        response = await read_cart_items_and_totals(
            user_id=user_id,
            session=session
        )
        break

    if response.cart_items:
        bill = response.total_price

        keyboard_build = InlineKeyboardBuilder()

        for item in response.cart_items:
            keyboard_build.row(
                InlineKeyboardButton(
                    text=(
                        f'{item.category_name} - '
                        f'{item.name} - '
                        f'{item.unit_price} ₹ - '
                        f'{item.quantity} шт'
                    ),
                    callback_data=CartEditCallbackFactory(
                        type_pr='plus',
                        product_id=item.product_id
                    ).pack()))

            keyboard_build.row(
                InlineKeyboardButton(
                    text='✖️',
                    callback_data=CartEditCallbackFactory(
                        type_pr='del',
                        product_id=item.product_id,
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='➖',
                    callback_data=CartEditCallbackFactory(
                        type_pr='minus',
                        product_id=item.product_id,
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='➕',
                    callback_data=CartEditCallbackFactory(
                        type_pr='plus',
                        product_id=item.product_id,
                    ).pack()
                ),
                width=3
            )

        keyboard_build.row(
            InlineKeyboardButton(
                text=f'Итого: {bill} ₹',
                callback_data='press_pass')
        )

        keyboard_build.row(
            InlineKeyboardButton(
                text='Главное меню',
                callback_data='press_main_menu'
            ),
            InlineKeyboardButton(
                text='Очистить',
                callback_data='press_empty'
            ),
            InlineKeyboardButton(
                text='Оформить',
                callback_data='press_cart'
            ),
            width=3
        )

        await callback.message.edit_text(
            text=LEXICON_RU['edit_cart'],
            reply_markup=keyboard_build.as_markup()
        )

        return {'status': 'success'}
    else:
        await callback.message.edit_text(
            text=LEXICON_RU['empty_cart'],
            reply_markup=await create_keyboard_main(callback.message.chat.id)
        )
        return {'status': 'success'}
