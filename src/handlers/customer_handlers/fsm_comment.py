from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from src.keyboards import fsm_comment_kb as keyboard, cart_kb
from src.callbacks import CartCallbackData
from src.state import FSMComment
from src.utils import cart_utils, redis_utils
from src.lexicons import (
    text_comment_ru,
    text_comment_en,
    text_common_ru,
    text_common_en,
    text_cart_ru,
    text_cart_en
)


router = Router(name=__name__)


@router.callback_query(CartCallbackData.filter(F.type_press == 'comment-cart'))
async def process_waiting_comment(
    callback: types.CallbackQuery,
    callback_data: CartCallbackData,
    state: FSMContext
):

    text_comment = (text_comment_ru
                    if callback.from_user.language_code == 'ru'
                    else text_comment_en)
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text=text_comment.create_comments_message(),
        reply_markup=keyboard.create_kb_fsm_comment(
            language=callback.from_user.language_code
        )
    )
    await state.update_data(store_id=callback_data.store_id)
    await state.set_state(FSMComment.waiting_comment)


@router.message(
    lambda x: x.text == text_common_en.common_dict['cancel'] or
    x.text == text_common_ru.common_dict['cancel'],
    ~StateFilter(default_state)
)
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    text_comment = (text_comment_ru
                    if message.from_user.language_code == 'ru'
                    else text_comment_en)
    await message.answer(
        text=text_comment.comment_dict['comment_input_cancelled'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    user_id = message.from_user.id

    data = await state.get_data()

    if message.from_user.language_code == 'ru':
        text_cart = text_cart_ru
    else:
        text_cart = text_cart_en

    order_comment = await redis_utils.get_data_from_redis(
        key_prefix='order_comment',
        user_id=user_id,
    )
    if order_comment:
        order_comment = order_comment['order_comment']

    message_text, bill = await cart_utils.update_cart_message(
        store_id=data['store_id'],
        user_id=user_id,
        order_comment=order_comment,
        language=message.from_user.language_code
    )

    reply_markup = cart_kb.create_kb_cart(
        store_id=data['store_id'],
        language=message.from_user.language_code,
        mess_id=message.message_id
    )

    if bill:
        await message.answer(
            text=message_text,
            reply_markup=reply_markup
        )
    else:
        await message.answer(
            text=text_cart.edit_cart_dict['empty_cart'],
            show_alert=True
        )

    await state.clear()


@router.message(FSMComment.waiting_comment, F.text)
async def process_comment_sent(
    message: types.Message,
    state: FSMContext
):
    text_common = (
        text_common_ru
        if message.from_user.language_code == 'ru'
        else text_common_en
    )

    user_id = message.from_user.id

    await state.update_data(order_comment=message.text)
    data = await state.get_data()

    await redis_utils.save_data_to_redis(
        key_prefix='order_comment',
        user_id=user_id,
        data=data
    )

    await message.answer(
        text=text_common.common_dict['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )

    if message.from_user.language_code == 'ru':
        text_cart = text_cart_ru
    else:
        text_cart = text_cart_en

    order_comment = await redis_utils.get_data_from_redis(
        key_prefix='order_comment',
        user_id=user_id,
    )
    if order_comment:
        order_comment = order_comment['order_comment']

    message_text, bill = await cart_utils.update_cart_message(
        store_id=data['store_id'],
        user_id=user_id,
        order_comment=order_comment,
        language=message.from_user.language_code
    )

    reply_markup = cart_kb.create_kb_cart(
        store_id=data['store_id'],
        language=message.from_user.language_code,
        mess_id=message.message_id
    )

    if bill:
        await message.answer(
            text=message_text,
            reply_markup=reply_markup
        )
    else:
        await message.answer(
            text=text_cart.edit_cart_dict['empty_cart'],
            show_alert=True
        )

    await state.clear()
