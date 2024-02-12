from aiogram import Bot
from aiogram.types import CallbackQuery

from src.db import order_db
from src.config import ADMINT_CHAT
from src.services import ORDER_TYPES, ORDER_STATUSES
from src.callbacks import (
    CreateOrderCallbackFactory,
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,
)
from src.keyboards import order_keyboards, main_keyboards
from src.lexicons import (
    generate_order_info_text,
    LEXICON_RU,
)
from src.utils import time_utils, order_utils
from src.fsm_state import user_dict_comment, user_dict


async def create_orders_takeaway(
    callback: CallbackQuery,
    callback_data: CreateOrderCallbackFactory,
    bot: Bot
):
    try:
        if time_utils.is_valid_time:
            order_type = callback_data.order_type

            order_info, chat_text, user_text = (
                await order_utils.create_new_orders(
                    callback_data=callback_data,
                    callback=callback
                )
            )
            await callback.message.edit_text(
                text=user_text,
                reply_markup=await main_keyboards.create_keyboard_main(
                    callback.message.chat.id
                )
            )

            await bot.send_message(
                chat_id=ADMINT_CHAT,
                text='❗️' + chat_text,
                reply_markup=order_keyboards.create_keyboard_check_order(
                    order_type=order_type,
                    order_id=order_info.order_id,
                    user_id=callback.message.chat.id,
                    mess_id=callback.message.message_id,
                )
            )
            if order_type == ORDER_TYPES['delivery']['id']:
                if (
                    order_info.delivery_latitude
                    and
                    order_info.delivery_latitude
                ):
                    await bot.send_location(
                        chat_id=ADMINT_CHAT,
                        longitude=order_info.delivery_latitude,
                        latitude=order_info.delivery_latitude
                    )
        else:
            await callback.answer(
                text=LEXICON_RU['non_working_hours'],
                show_alert=True
            )
    finally:
        user_dict.pop(callback.message.chat.id, None)
        user_dict_comment.pop(callback.message.chat.id, None)


async def process_edit_status_order(
    callback: CallbackQuery,
    callback_data: CheckOrdersCallbackFactory,
    bot: Bot
):
    order_status = await order_utils.get_status_name_by_id(
        callback_data.status
    )
    user_id = callback_data.user_id
    delivery_time = await order_db.update_order_status(
        order_status=order_status,
        order_id=callback_data.order_id,
        order_type=callback_data.order_type
    )

    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    text = await order_utils.create_text(
        callback_data=callback_data,
        callback=callback
    )

    user_text = await generate_order_info_text(callback_data=callback_data)

    message_id = await bot.send_message(
        chat_id=user_id,
        text=user_text,
        reply_markup=await main_keyboards.create_keyboard_main(
            user_id
        )
    )

    keyboard = order_keyboards.create_keyboard_time_cooking(
        data=callback_data,
        mess_id=message_id.message_id,
        time_del=delivery_time,
    )

    if order_status == ORDER_STATUSES['cancelled']['name']:
        await callback.message.edit_text(
            text='❗️⛔️' + text,
            reply_markup=None
        )
        await callback.message.answer(
            text=user_text + '\n' + '❗️⛔️'*6
        )

    else:
        await callback.message.edit_text(
            text='❗️' + text,
            reply_markup=keyboard
        )


async def process_time_order(
    callback: CallbackQuery,
    callback_data: TimeOrdersCallbackFactory,
    bot: Bot
):
    user_id = callback_data.user_id
    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    text = await order_utils.create_text(
        callback_data=callback_data,
        callback=callback
    )

    message_id = await bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=await main_keyboards.create_keyboard_main(user_id)
    )

    if callback_data.order_type == ORDER_TYPES['takeaway']['id']:
        keyboard = order_keyboards.create_order_status_keyboard(
            data=callback_data,
            mess_id=message_id.message_id,
        )
    else:
        keyboard = order_keyboards.create_order_status_delivery_keyboard(
            data=callback_data,
            mess_id=message_id.message_id,
        )

    await callback.message.edit_reply_markup(
        reply_markup=keyboard
    )


async def process_edit_status_redy_order(
    callback: CallbackQuery,
    callback_data: OrderStatusCallbackFactory,
    bot: Bot
):
    order_status = await order_utils.get_status_name_by_id(
        callback_data.status
    )
    user_id = callback_data.user_id
    await order_db.update_order_status(
        order_status=order_status,
        order_id=callback_data.order_id,
    )

    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    text = await order_utils.create_text(
        callback_data=callback_data,
        callback=callback
    )

    user_text = await generate_order_info_text(callback_data=callback_data)

    message_id = await bot.send_message(
        chat_id=user_id,
        text=user_text,
        reply_markup=await main_keyboards.create_keyboard_main(user_id)
    )

    keyboard = order_keyboards.create_status_redy_order_keyboard(
        data=callback_data,
        mess_id=message_id.message_id,
    )

    if order_status == ORDER_STATUSES['completed']['name']:
        await callback.message.edit_text(
            text='✅' + text,
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            text='❗️' + text,
            reply_markup=keyboard
        )


async def process_open_account(callback: CallbackQuery,):

    keyboard = await order_keyboards.account_keyboards.create_keyboard_account(
        user_id=callback.message.chat.id
    )

    await callback.message.answer(
        text='Я тут',
        reply_markup=keyboard
    )
