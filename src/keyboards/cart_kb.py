from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import LEXICON_RU
from src.callbacks import CartEditCallbackFactory
from .main_kb import create_kb_main
from src.db import cart_db
from src.lexicons import text_cart_en, text_cart_ru


def create_kb_cart(mess_id: int, language: str):
    if language == 'ru':
        text_cart = text_cart_ru
    else:
        text_cart = text_cart_en

    cart_text_dict = text_cart.create_btn_cart(
        mess_id=mess_id, language=language)

    keyboard = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(
        text=value['text'],
        callback_data=value['callback_data']
    ) for value in cart_text_dict.values()]

    row_lengths = [1, 3, 3]

    current_index = 0
    for row_length in row_lengths:
        row_buttons = buttons[current_index:current_index + row_length]
        keyboard.row(*row_buttons, width=row_length)
        current_index += row_length

    return keyboard.as_markup()


async def create_kbs_products_cart(
        callback,
        user_id: int,
        language: str
):

    cart_info = await cart_db.get_cart_items_and_totals(
        user_id=user_id
    )

    if language == 'ru':
        text_cart = text_cart_ru.edit_cart_dict
        edit_btn_cart = text_cart_ru.edit_btn_cart_dict
        create_total = text_cart_ru.create_total_btn
    else:
        text_cart = text_cart_en.edit_cart_dict
        edit_btn_cart = text_cart_en.edit_btn_cart_dict
        create_total = text_cart_en.create_total_btn

    if cart_info.cart_items:
        bill = cart_info.total_price

        keyboard = InlineKeyboardBuilder()

        for item in cart_info.cart_items:
            product_name = item.name_rus if language == 'ru' else item.name_en
            category_name = item.category_name_rus if language == 'ru' else item.category_name_en
            unit_price = 'Сумма' if language == 'ru' else 'Unit price'
            piece = 'шт' if language == 'ru'else 'pc'
            keyboard.row(
                InlineKeyboardButton(
                    text=(
                        f'{category_name} - '
                        f'{product_name} - '
                    ),
                    callback_data=CartEditCallbackFactory(
                        type_pr='plus',
                        product_id=item.product_id
                    ).pack()))
            keyboard.row(
                InlineKeyboardButton(
                    text=f'{unit_price}: {item.unit_price} ₹',
                    callback_data='press_pass'
                ),
                InlineKeyboardButton(
                    text=f'{item.quantity} {piece}',
                    callback_data='press_pass'),
                width=2
            )

            keyboard.row(
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
        create_total_dict = create_total(bill)

        button_total = [InlineKeyboardButton(
            text=value['text'],
            callback_data=value['callback_data']
        ) for value in create_total_dict.values()]

        keyboard.row(*button_total)

        buttons = [InlineKeyboardButton(
            text=value['text'],
            callback_data=value['callback_data']
        ) for value in edit_btn_cart.values()]

        keyboard.row(*buttons, width=3)

        await callback.message.edit_text(
            text=text_cart['edit_cart'],
            reply_markup=keyboard.as_markup()
        )

        return {'status': 'success'}
    else:
        await callback.message.edit_text(
            text=text_cart['empty_cart'],
            reply_markup=await create_kb_main(
                language=callback.from_user.language_code,
                user_id=callback.message.chat.id)
        )
        return {'status': 'success'}
