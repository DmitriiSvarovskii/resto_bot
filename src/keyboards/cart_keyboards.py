from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import LEXICON_RU
from src.callbacks import CartEditCallbackFactory
from .main_keyboards import create_keyboard_main
from src.db import cart_db
from src.lexicons import cart_test_text


def create_keyboard_cart(mess_id: int):
    my_dict = cart_test_text.my_func(mess_id=mess_id)

    keyboard = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(
        text=value['text'],
        callback_data=value['callback_data']
    ) for value in my_dict.values()]

    row_lengths = [1, 2, 3]

    current_index = 0
    for row_length in row_lengths:
        row_buttons = buttons[current_index:current_index + row_length]
        keyboard.row(*row_buttons, width=row_length)
        current_index += row_length

    return keyboard.as_markup()


async def create_keyboards_products_cart(callback, user_id):

    cart_info = await cart_db.get_cart_items_and_totals(
        user_id=user_id
    )

    if cart_info.cart_items:
        bill = cart_info.total_price

        keyboard_build = InlineKeyboardBuilder()

        for item in cart_info.cart_items:
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
