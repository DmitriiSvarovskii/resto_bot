from typing import Union
from aiogram.types import CallbackQuery, Message


from src.database import get_async_session
from src.crud import read_cart_items_and_totals
from src.keyboards import create_keyboard_cart
from src.lexicons import cart_text, LEXICON_RU


async def update_cart_message(
    user_id: int,
    message: Union[CallbackQuery, Message],
    comment=None
) -> None:
    async for session in get_async_session():
        response = await read_cart_items_and_totals(
            user_id=user_id,
            session=session
        )
        break

    bill = response.total_price
    order_text = ''

    for item in response.cart_items:
        order_text += (
            f'{item.category_name} - {item.name} x {item.quantity} - {item.unit_price} ₹\n\n'
        )

    message_text = cart_text(
        bill=bill,
        order_text=order_text,
        comment=comment
    )

    if bill:
        if isinstance(message, CallbackQuery):
            await message.message.edit_text(
                text=message_text,
                reply_markup=create_keyboard_cart(
                    mess_id=message.message.message_id
                )
            )
        else:
            await message.answer(
                text=message_text,
                reply_markup=create_keyboard_cart(
                    mess_id=message.message_id
                )
            )
    else:
        if isinstance(message, CallbackQuery):
            await message.answer(
                text=LEXICON_RU['empty_cart'],
                show_alert=True
            )
        else:
            await message.answer(
                text=LEXICON_RU['empty_cart'],
                show_alert=True
            )


def get_comment_value(user_id, user_dict_comment):
    if (user_id in user_dict_comment and
            "comment" in user_dict_comment[user_id]):
        return user_dict_comment[user_id]["comment"]
    else:
        return None


def get_user_info(user_id, user_dict):
    if user_id in user_dict:
        return user_dict[user_id]
    else:
        return None
