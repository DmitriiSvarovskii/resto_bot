from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from src.state import FSMDeliveryInfo, user_dict
from src.callbacks import DeliveryIdCallbackFactory
from src.db import delivery_db
from src.config import settings
from src.utils import time_utils
from src.keyboards import delivery_kb, main_kb
from src.lexicons import (
    text_fsm_delivery_ru,
    text_fsm_delivery_en,
    text_menu_ru,
    text_menu_en,
    text_common_ru,
    text_common_en,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_delivery_pay')
async def handle_delivery_form_command(
    callback: types.CallbackQuery,
    state: FSMContext
):
    if settings.MODE == 'PROD':
        if await time_utils.is_valid_time():
            await process_delivery_form_command(
                callback=callback,
                state=state
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
        await process_delivery_form_command(
            callback=callback,
            state=state
        )


async def process_delivery_form_command(
    callback: types.CallbackQuery,
    state: FSMContext
):
    text_delivery = (text_fsm_delivery_ru
                     if callback.from_user.language_code == 'ru'
                     else text_fsm_delivery_en)

    delivery_disctricts = await delivery_db.get_delivery_districts()

    keyboard = await delivery_kb.create_kb_delivery(
        delivery_districts=delivery_disctricts,
        language=callback.from_user.language_code,
    )

    await callback.message.edit_text(
        text=text_delivery.delivery_fsm_text['delivery_districts'],
        reply_markup=keyboard
    )

    await state.set_state(FSMDeliveryInfo.waiting_delivery_id)


@router.message(
    lambda x: x.text == text_common_en.common_dict['cancel'] or
    x.text == text_common_ru.common_dict['cancel'],
    ~StateFilter(default_state)
)
async def process_cancel_command_delivery(
    message: types.Message,
    state: FSMContext
):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    await message.answer(
        text=text.delivery_fsm_text['abort_delivery'],
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()
    await message.answer(
        text=text.delivery_fsm_text['order_saved_message'],
        reply_markup=await main_kb.create_kb_main(
            language=message.from_user.language_code,
            user_id=message.chat.id
        )
    )


@router.callback_query(
    FSMDeliveryInfo.waiting_delivery_id,
    DeliveryIdCallbackFactory.filter()
)
async def process_district_selection(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: DeliveryIdCallbackFactory
):
    if callback.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    await state.update_data(delivery_id=callback_data.delivery_id)

    if callback.message:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

    await callback.message.answer(
        text=text.delivery_fsm_text['phone_input'],
        reply_markup=delivery_kb.create_kb_delivery_fsm(
            language=callback.from_user.language_code
        )
    )
    await state.set_state(FSMDeliveryInfo.waiting_number_phone)


@router.message(FSMDeliveryInfo.waiting_delivery_id)
async def warning_not_number(message: types.Message):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    delivery_disctricts = await delivery_db.get_delivery_districts()

    keyboard = await delivery_kb.create_kb_delivery(
        delivery_disctricts
    )

    await message.answer(
        text=text.delivery_fsm_text['use_buttons_for_districts'],
        reply_markup=keyboard
    )


@router.message(FSMDeliveryInfo.waiting_number_phone,
                (lambda x: x.text.isdigit() and len(x.text)
                 == 10 or x.text == text_common_en.common_dict['skip'] or
                 x.text == text_common_ru.common_dict['skip']))
async def process_phone_sent(
    message: types.Message,
    state: FSMContext
):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    if message.text == text.delivery_fsm_text['skip']:
        await state.update_data(
            customer_phone=text.delivery_fsm_text['not_specified']
        )
    else:
        await state.update_data(customer_phone=message.text)

    await message.answer(
        text=text.delivery_fsm_text['delivery_comment_prompt'],
        reply_markup=delivery_kb.create_kb_delivery_fsm(
            language=message.from_user.language_code)
    )

    await state.set_state(FSMDeliveryInfo.waiting_guide)


@router.message(FSMDeliveryInfo.waiting_number_phone)
async def warning_not_phone(message: types.Message):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    await message.answer(
        text=text.delivery_fsm_text['phone_number_error_message'],
        reply_markup=delivery_kb.create_kb_delivery_fsm(
            language=message.from_user.language_code)
    )


@router.message(FSMDeliveryInfo.waiting_guide, F.text)
async def process_guide_sent(
    message: types.Message,
    state: FSMContext
):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    if message.text == text.delivery_fsm_text['skip']:
        await state.update_data(
            delivery_comment=text.delivery_fsm_text['not_specified']
        )
    else:
        await state.update_data(delivery_comment=message.text)

    await message.answer(
        text=text.delivery_fsm_text['location_request_step'],
        reply_markup=delivery_kb.create_kb_delivery_fsm_location(
            language=message.from_user.language_code)
    )

    await state.set_state(FSMDeliveryInfo.waiting_location)


@router.message(FSMDeliveryInfo.waiting_guide)
async def warning_not_guide(message: types.Message):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    await message.answer(
        text=text.delivery_fsm_text['error_comment'],
        reply_markup=delivery_kb.create_kb_delivery_fsm(
            language=message.from_user.language_code)
    )


@router.message(
    FSMDeliveryInfo.waiting_location,
    lambda x: x.location or x.text == text_common_en.common_dict['skip'] or
    x.text == text_common_ru.common_dict['skip']
)
async def process_location_sent(
    message: types.Message,
    state: FSMContext
):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    if message.location:
        await state.update_data(
            delivery_latitude=message.location.latitude,
            delivery_longitude=message.location.longitude
        )
    await message.answer(
        text=text.delivery_fsm_text['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(
        text=text.delivery_fsm_text['done_fsm_delivery'],
        reply_markup=delivery_kb.create_kb_delivery_go(
            mess_id=message.message_id,
            language=message.from_user.language_code
        )
    )

    user_dict[message.chat.id] = await state.get_data()
    await state.clear()


@router.message(FSMDeliveryInfo.waiting_location)
async def warning_not_location(message: types.Message):
    if message.from_user.language_code == 'ru':
        text = text_fsm_delivery_ru
    else:
        text = text_fsm_delivery_en
    await message.answer(
        text=text.delivery_fsm_text['error_location'],
        reply_markup=delivery_kb.create_kb_delivery_fsm(
            language=message.from_user.language_code)
    )
