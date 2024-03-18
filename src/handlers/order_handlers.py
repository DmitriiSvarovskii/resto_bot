from aiogram import Bot, Router, F, types

from src.db import order_db, store_db
from src.services import ORDER_TYPES, ORDER_STATUSES
from src.callbacks import (
    CreateOrderCallbackFactory,
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,
)
from src.keyboards import main_kb, order_kb
from src.lexicons import (
    generate_order_info_text,
    generate_order_info_time_text,
    LEXICON_RU,
)
from src.utils import time_utils, order_utils
from src.state import user_dict_comment, user_dict


router = Router(name=__name__)


@router.callback_query(CreateOrderCallbackFactory.filter())
async def create_orders_takeaway(
    callback: types.CallbackQuery,
    callback_data: CreateOrderCallbackFactory,
    bot: Bot
):
    try:
        if await time_utils.is_valid_time():
            order_type = callback_data.order_type

            order_info, chat_text, user_text = (
                await order_utils.create_new_orders(
                    callback_data=callback_data,
                    callback=callback
                )
            )
            await callback.message.edit_text(
                text=user_text,
                reply_markup=await main_kb.create_kb_main(
                    callback.message.chat.id
                )
            )
            store_info = await store_db.get_store_info()
            await bot.send_message(
                chat_id=store_info.manager_group,
                text='❗️' + chat_text,
                reply_markup=order_kb.create_kb_check_order(
                    order_type=order_type,
                    order_id=order_info.order_id,
                    user_id=callback.message.chat.id,
                    mess_id=callback.message.message_id,
                )
            )
            if order_type == ORDER_TYPES['delivery']['id']:
                if (
                    order_info.delivery_longitude
                    and
                    order_info.delivery_latitude
                ):
                    await bot.send_location(
                        chat_id=store_info.manager_group,
                        longitude=order_info.delivery_longitude,
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


@router.callback_query(CheckOrdersCallbackFactory.filter())
async def process_edit_status_order(
    callback: types.CallbackQuery,
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

    if callback.message.reply_markup:
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
        reply_markup=await main_kb.create_kb_main(
            user_id
        )
    )

    keyboard = order_kb.create_kb_time_cooking(
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


@router.callback_query(TimeOrdersCallbackFactory.filter())
async def process_time_order(
    callback: types.CallbackQuery,
    callback_data: TimeOrdersCallbackFactory,
    bot: Bot
):
    user_id = callback_data.user_id

    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    user_text = generate_order_info_time_text(
        callback_data=callback_data
    )
    # text = await order_utils.create_text(
    #     callback_data=callback_data,
    #     callback=callback
    # )

    message_id = await bot.send_message(
        chat_id=user_id,
        text=user_text,
        reply_markup=await main_kb.create_kb_main(user_id)
    )

    if callback_data.order_type == ORDER_TYPES['takeaway']['id']:
        keyboard = order_kb.create_order_status_keyboard(
            data=callback_data,
            mess_id=message_id.message_id,
        )
    else:
        keyboard = order_kb.create_order_status_delivery_keyboard(
            data=callback_data,
            mess_id=message_id.message_id,
        )

    await callback.message.edit_reply_markup(
        reply_markup=keyboard
    )


@router.callback_query(OrderStatusCallbackFactory.filter())
async def process_edit_status_redy_order(
    callback: types.CallbackQuery,
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
        reply_markup=await main_kb.create_kb_main(user_id)
    )

    keyboard = order_kb.create_status_redy_order_keyboard(
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


@router.callback_query(F.data == 'press_account')
async def process_open_account(callback: types.CallbackQuery,):

    keyboard = await order_kb.account_keyboards.create_kb_account(
        user_id=callback.message.chat.id
    )

    await callback.message.answer(
        text='Я тут',
        reply_markup=keyboard
    )
