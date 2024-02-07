from aiogram import Bot
from aiogram.types import CallbackQuery

from src.utils import create_new_orders, create_text, get_status_name_by_id
from src.crud import update_order_status
from src.database import get_async_session
from src.db import order_db
from src.config import ADMINT_CHAT
from src.services import ORDER_TYPES, ORDER_STATUSES
from src.callbacks import (
    CreateOrderCallbackFactory,
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,
)
from src.keyboards import (
    create_keyboard_main,
    create_keyboard_check_order,
    create_keyboard_time_cooking,
    create_order_status_keyboard,
    create_order_status_delivery_keyboard,
    create_status_redy_order_keyboard,
    account_keyboards,
)
from src.lexicons import (
    generate_order_info_text,
    generate_order_info_time_text,
    LEXICON_RU,
)
from src.utils_new import time_utils


async def create_orders_takeaway(
    callback: CallbackQuery,
    callback_data: CreateOrderCallbackFactory,
    bot: Bot
):
    if time_utils.is_valid_time():
        order_type = callback_data.order_type

        order_id, chat_text, user_text = await create_new_orders(
            order_type=order_type,
            status=callback_data.status,
            callback=callback
        )

        await callback.message.edit_text(
            text=user_text,
            reply_markup=await create_keyboard_main(callback.message.chat.id)
        )

        await bot.send_message(
            chat_id=ADMINT_CHAT,
            text='❗️' + chat_text,
            reply_markup=create_keyboard_check_order(
                order_type=order_type,
                order_id=order_id,
                user_id=callback.message.chat.id,
                mess_id=callback.message.message_id,
            )
        )
        # if order_type == "Доставка":
        #     if latitude and longitude:
        #         await bot.send_location(
        #             chat_id=ADMINT_CHAT,
        #             longitude=longitude,
        #             latitude=latitude
        #         )
        #     else:
        #         await bot.send_message(
        #             chat_id=ADMINT_CHAT,
        #             text="longitude"
        #         )
    else:
        await callback.answer(
            text=LEXICON_RU['non_working_hours'],
            show_alert=True
        )


async def process_edit_status_order(
    callback: CallbackQuery,
    callback_data: CheckOrdersCallbackFactory,
    bot: Bot
):
    order_status = await get_status_name_by_id(callback_data.status)
    delivery_time = None

    async for session in get_async_session():
        await update_order_status(
            order_status=order_status,
            order_id=callback_data.order_id,
            session=session
        )
        if callback_data.order_type == ORDER_TYPES['delivery']['id']:
            delivery_time = await order_db.get_delivery_time(
                order_id=callback_data.order_id,
            )
        break

    await bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    text = await create_text(callback_data=callback_data)

    user_text = await generate_order_info_text(callback_data=callback_data)

    message_id = await bot.send_message(
        chat_id=callback_data.user_id,
        text=user_text,
        reply_markup=await create_keyboard_main(callback_data.user_id)
    )
    keyboard = create_keyboard_time_cooking(
        order_type=callback_data.order_type,
        order_id=callback_data.order_id,
        user_id=callback_data.user_id,
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

    await bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    text = generate_order_info_time_text(callback_data=callback_data)

    message_id = await bot.send_message(
        chat_id=callback_data.user_id,
        text=text,
        reply_markup=await create_keyboard_main(callback_data.user_id)
    )

    if callback_data.order_type == ORDER_TYPES['takeaway']['id']:
        keyboard = create_order_status_keyboard(
            order_type=callback_data.order_type,
            order_id=callback_data.order_id,
            user_id=callback_data.user_id,
            mess_id=message_id.message_id,
        )
    else:
        keyboard = create_order_status_delivery_keyboard(
            order_type=callback_data.order_type,
            order_id=callback_data.order_id,
            user_id=callback_data.user_id,
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
    order_status = await get_status_name_by_id(callback_data.status)

    async for session in get_async_session():
        await update_order_status(
            order_status=order_status,
            order_id=callback_data.order_id,
            session=session
        )
        break

    await bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    text = await create_text(callback_data=callback_data)

    user_text = await generate_order_info_text(callback_data=callback_data)

    message_id = await bot.send_message(
        chat_id=callback_data.user_id,
        text=user_text,
        reply_markup=await create_keyboard_main(callback_data.user_id)
    )

    keyboard = create_status_redy_order_keyboard(
        order_type=callback_data.order_type,
        order_id=callback_data.order_id,
        user_id=callback_data.user_id,
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

    keyboard = await account_keyboards.create_keyboard_account(
        user_id=callback.message.chat.id
    )

    await callback.message.answer(
        text='Я тут',
        reply_markup=keyboard
    )
