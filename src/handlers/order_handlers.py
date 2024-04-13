from aiogram import Bot, Router, types, F
from aiogram.exceptions import TelegramBadRequest

from src.config import settings
from src.db import order_db, store_db
from src.keyboards import main_kb, order_kb, account_kb
from src.utils import time_utils, order_utils, report_utils
from src.state import user_dict_comment, user_dict
from src.callbacks import (
    AccountOrdersCbData,
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,
)
from src.callbacks.order import OrderCallbackFactory
from src.lexicons import (
    text_order_ru,
    text_order_en,
    text_menu_ru,
    text_menu_en,
    text_main_menu_ru,
    text_main_menu_en,
)
from src.utils import OrderStatus, OrderTypes


router = Router(name=__name__)


# @router.callback_query(CreateOrderCallbackFactory.filter())
@router.callback_query(OrderCallbackFactory.filter(F.type_callback == 'create'))
async def process_orders(callback: types.CallbackQuery,
                         callback_data: OrderCallbackFactory,
                         #  callback_data: CreateOrderCallbackFactory,
                         bot: Bot):
    if settings.MODE == 'PROD':
        if await time_utils.is_valid_time():
            await create_orders_takeaway(
                callback=callback,
                callback_data=callback_data,
                bot=bot,
            )
        else:
            if callback.from_user.language_code == 'ru':
                text_menu = text_menu_ru
            else:
                text_menu = text_menu_en
            await callback.answer(
                text=text_menu.menu_messages_dict['non_working_hours'],
                show_alert=True
            )
    else:
        await create_orders_takeaway(
            callback=callback,
            callback_data=callback_data,
            bot=bot,
        )


async def create_orders_takeaway(
    callback: types.CallbackQuery,
    callback_data: OrderCallbackFactory,
    bot: Bot
):
    try:
        order_type = callback_data.order_type

        order_info, chat_text, user_text = (
            await order_utils.create_new_orders(
                callback_data=callback_data,
                callback=callback,
                language=callback.from_user.language_code
            )
        )
        await callback.message.edit_text(
            text=user_text,
            reply_markup=await main_kb.create_kb_main(
                language=callback.from_user.language_code,
                user_id=callback.message.chat.id
            )
        )

        store_info = await store_db.get_store_info()

        message_data = await bot.send_message(
            chat_id=store_info.manager_group,
            text='❗️' + chat_text,
            reply_markup=order_kb.create_kb_check_order(
                order_type=order_type,
                order_id=order_info.order_id,
                user_id=callback.message.chat.id,
                mess_id=callback.message.message_id,
                language=callback_data.language
            )
        )

        await order_utils.create_order_messages_id(
            order_id=order_info.order_id,
            message_id=message_data.message_id
        )

        if order_type in OrderTypes.DELIVERY.value.values():
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
    finally:
        user_dict.pop(callback.message.chat.id, None)
        user_dict_comment.pop(callback.message.chat.id, None)


@router.callback_query(CheckOrdersCallbackFactory.filter())
async def process_edit_status_order(
    callback: types.CallbackQuery,
    callback_data: CheckOrdersCallbackFactory,
    bot: Bot
):
    if callback_data.language == 'ru':
        text_order = text_order_ru
    else:
        text_order = text_order_en

    order_status = OrderStatus.get_name_by_id(
        target_id=callback_data.status,
        language=callback_data.language
    )

    user_id = callback_data.user_id
    delivery_time = await order_db.update_order_status(
        order_status=order_status,
        order_id=callback_data.order_id,
        order_type=callback_data.order_type
    )

    try:
        if callback.message.reply_markup:
            await bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=callback_data.mess_id,
                reply_markup=None
            )
    except TelegramBadRequest:
        pass

    text = await order_utils.create_text(
        callback_data=callback_data,
        language=callback.from_user.language_code
    )

    user_text = await text_order.generate_update_order_info_text(
        order_status=order_status,
        order_id=callback_data.order_id
    )

    message_id = await bot.send_message(
        chat_id=user_id,
        text=user_text,
        reply_markup=await main_kb.create_kb_main(
            language=callback_data.language,
            user_id=user_id
        )
    )

    keyboard = order_kb.create_kb_time_cooking(
        data=callback_data,
        mess_id=message_id.message_id,
        time_del=delivery_time,
        language=callback_data.language
    )
    if order_status in OrderStatus.CANCELLED.value.values():
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
    if callback_data.language == 'ru':
        text_order = text_order_ru
    else:
        text_order = text_order_en

    user_id = callback_data.user_id

    try:
        if callback.message.reply_markup:
            await bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=callback_data.mess_id,
                reply_markup=None
            )
    except TelegramBadRequest:
        pass

    user_text = text_order.generate_order_info_time_text(
        callback_data=callback_data
    )

    message_id = await bot.send_message(
        chat_id=user_id,
        text=user_text,
        reply_markup=await main_kb.create_kb_main(
            language=callback_data.language,
            user_id=user_id
        )
    )

    if callback_data.order_type in OrderTypes.DELIVERY.value.values():
        keyboard = order_kb.create_order_status_delivery_keyboard(
            data=callback_data,
            mess_id=message_id.message_id,
            language=callback_data.language
        )
    else:
        keyboard = order_kb.create_order_status_keyboard(
            data=callback_data,
            mess_id=message_id.message_id,
            language=callback_data.language
        )

    await callback.message.edit_reply_markup(
        reply_markup=keyboard
    )


@router.callback_query(
    AccountOrdersCbData.filter(
        F.type_callback == 'order-details'
    )
)
async def process_order_details_in_account(
    callback: types.CallbackQuery,
    callback_data: AccountOrdersCbData,
):
    try:
        text = await report_utils.generate_view_order_text(
            order_id=callback_data.order_id
        )

        keyboard = await account_kb.create_kb_account(
            user_id=callback.message.chat.id,
            language=callback.from_user.language_code
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    except Exception as e:
        print(e)
        await callback.answer(
            text="повторный запрос"
        )


@router.callback_query(
    OrderStatusCallbackFactory.filter(
        F.type_callback == 'cancel-acc'
    )
)
async def process_cancel_order_in_account(
    callback: types.CallbackQuery,
    callback_data: OrderStatusCallbackFactory,
    bot: Bot
):
    if callback_data.language == 'ru':
        text_order = text_order_ru
        text_main_menu = text_main_menu_ru
    else:
        text_order = text_order_en
        text_main_menu = text_main_menu_en

    order_status = OrderStatus.get_name_by_id(
        target_id=callback_data.status,
        language=callback_data.language
    )
    await order_db.update_order_status(
        order_status=order_status,
        order_id=callback_data.order_id,
        order_type=callback_data.order_type
    )

    text = await order_utils.create_text(
        callback_data=callback_data,
        language=callback.from_user.language_code
    )

    user_text = await text_order.generate_update_order_info_text(
        order_status=order_status,
        order_id=callback_data.order_id
    )

    store_info = await store_db.get_store_info()

    await bot.edit_message_text(
        chat_id=store_info.manager_group,
        text='❗️⛔️' + text,
        message_id=callback_data.mess_id,
        reply_markup=None
    )

    await bot.send_message(
        chat_id=store_info.manager_group,
        text=user_text + '\n' + '❗️⛔️'*6,
    )
    keyboard = await account_kb.create_kb_account(
        user_id=callback.message.chat.id,
        language=callback.from_user.language_code
    )
    await callback.message.edit_reply_markup(
        text=text_main_menu.main_menu_dict['personal_area'],
        reply_markup=keyboard
    )
    await callback.answer(
        text=f"ЗАКАЗ № {callback_data.order_id} ОТМЕНЁН!!!",
        show_alert=True
    )


@router.callback_query(OrderStatusCallbackFactory.filter())
async def process_edit_status_redy_order(
    callback: types.CallbackQuery,
    callback_data: OrderStatusCallbackFactory,
    bot: Bot
):
    if callback_data.language == 'ru':
        text_order = text_order_ru
    else:
        text_order = text_order_en
    order_status = OrderStatus.get_name_by_id(
        target_id=callback_data.status,
        language=callback_data.language
    )
    # order_status = await order_utils.get_status_name_by_id(
    #     callback_data.status
    # )
    user_id = callback_data.user_id
    await order_db.update_order_status(
        order_status=order_status,
        order_id=callback_data.order_id,
    )

    try:
        if callback.message.reply_markup:
            await bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=callback_data.mess_id,
                reply_markup=None
            )
    except TelegramBadRequest:
        pass

    text = await order_utils.create_text(
        callback_data=callback_data,
        language=callback.from_user.language_code
    )

    user_text = await text_order.generate_update_order_info_text(
        order_status=order_status,
        order_id=callback_data.order_id
    )

    message_id = await bot.send_message(
        chat_id=user_id,
        text=user_text,
        reply_markup=await main_kb.create_kb_main(
            language=callback_data.language,
            user_id=user_id
        )
    )

    keyboard = order_kb.create_status_redy_order_keyboard(
        data=callback_data,
        mess_id=message_id.message_id,
        language=callback_data.language
    )

    if order_status in OrderStatus.COMPLETED.value.values():
        await callback.message.edit_text(
            text='✅' + text,
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            text='❗️' + text,
            reply_markup=keyboard
        )
