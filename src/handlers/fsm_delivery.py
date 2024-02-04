from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from ..fsm_state import FSMDeliveryInfo, user_dict
from ..callbacks import DeliveryIdCallbackFactory
from ..lexicons import LEXICON_RU
from ..services import is_valid_time
from ..utils import get_delivery_districts
from ..keyboards import (
    create_keyboard_delivery,
    create_keyboard_main,
    create_keyboard_delivery_fsm,
    create_keyboard_delivery_go,
    create_keyboard_delivery_fsm_location,
)

storage: MemoryStorage = MemoryStorage()


async def process_delivery_form_command(
    callback: CallbackQuery,
    state: FSMContext
):
    if is_valid_time():
        delivery_disctricts = await get_delivery_districts()

        keyboard = await create_keyboard_delivery(delivery_disctricts)

        await callback.message.edit_text(
            text=LEXICON_RU['delivery_districts'],
            reply_markup=keyboard
        )

        await state.set_state(FSMDeliveryInfo.waiting_delivery_id)
    else:
        await callback.answer(
            text=LEXICON_RU['closing_time'],
            show_alert=True
        )


async def process_cancel_command_delivery(
    message: Message,
    state: FSMContext
):
    await message.answer(
        text=LEXICON_RU['abort_delivery'],
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()

    await message.answer(
        text=LEXICON_RU['order_saved_message'],
        reply_markup=await create_keyboard_main(message.chat.id)
    )


async def process_district_selection(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: DeliveryIdCallbackFactory
):
    await state.update_data(delivery_id=callback_data.delivery_id)

    if callback.message:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

    await callback.message.answer(
        text=LEXICON_RU['phone_input'],
        reply_markup=create_keyboard_delivery_fsm()
    )
    await state.set_state(FSMDeliveryInfo.waiting_number_phone)


async def warning_not_number(message: Message):
    delivery_disctricts = await get_delivery_districts()

    keyboard = await create_keyboard_delivery(delivery_disctricts)

    await message.answer(
        text=LEXICON_RU['use_buttons_for_districts'],
        reply_markup=keyboard
    )


async def process_phone_sent(
    message: Message,
    state: FSMContext
):
    if message.text == LEXICON_RU['skip']:
        await state.update_data(number_phone='не указан')
    else:
        await state.update_data(number_phone=message.text)

    await message.answer(
        text=LEXICON_RU['delivery_comment_prompt'],
        reply_markup=create_keyboard_delivery_fsm()
    )

    await state.set_state(FSMDeliveryInfo.waiting_guide)


async def warning_not_phone(message: Message):
    await message.answer(
        text=LEXICON_RU['phone_number_error_message'],
        reply_markup=create_keyboard_delivery_fsm()
    )


async def process_guide_sent(
    message: Message,
    state: FSMContext
):
    if message.text == LEXICON_RU['skip']:
        await state.update_data(guide='не указан')
    else:
        await state.update_data(guide=message.text)

    await message.answer(
        text=LEXICON_RU['location_request_step'],
        reply_markup=create_keyboard_delivery_fsm_location()
    )

    await state.set_state(FSMDeliveryInfo.waiting_location)


async def warning_not_guide(message: Message):
    await message.answer(
        text=LEXICON_RU['error_comment'],
        reply_markup=create_keyboard_delivery_fsm()
    )


async def process_location_sent(
    message: Message,
    state: FSMContext
):
    if message.location:
        await state.update_data(
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=LEXICON_RU['done_fsm_delivery'],
        reply_markup=create_keyboard_delivery_go(
            mess_id=message.message_id
        )
    )

    user_dict[message.chat.id] = await state.get_data()
    await state.clear()


async def warning_not_location(message: Message):
    await message.answer(
        text=LEXICON_RU['error_location'],
        reply_markup=create_keyboard_delivery_fsm()
    )
