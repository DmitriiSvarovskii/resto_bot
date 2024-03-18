from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.db import delivery_db, category_db
from src.keyboards import (
    admin_kb,
    category_kb,

)
from src.utils import delivery_utils
from .change_delivery_base import process_edit_delivery_message
from src.state import FSMDeliveryAdmin
from src.callbacks import (
    CategoryAdminAddCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_add_new_district')
async def process_add_new_district(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.answer(
        text='Введите название нового района доставки',
    )
    await state.set_state(FSMDeliveryAdmin.waiting_name)


@router.message(F.text == 'отменить')
async def process_cancel_command_state_order(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Вы отменили добавление нового района доставки',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await message.answer(
        text='Выберите пункт меню',
        reply_markup=admin_kb.create_kb_edit_menu()
    )


@router.message(FSMDeliveryAdmin.waiting_name, F.text)
async def process_waiting_category_id(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(
        name=message.text
    )
    await message.answer(
        text='Введите стоимость доставки в этот район',
    )
    await state.set_state(FSMDeliveryAdmin.waiting_price)


@router.message(FSMDeliveryAdmin.waiting_name)
async def process_waiting_district_name(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Произошла ошибка. Пожалуйста пришлите цену доставки. Цену укажите цифрами, без дополнительных знаков и символов',
    )


@router.message(FSMDeliveryAdmin.waiting_price, F.text.isdigit())
async def process_waiting_district_name(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(price=int(message.text))
    await message.answer(
        text='Введите время доставки (укажите время доставки с момента, когда курьеру передели заказ, время укажите в минутах.)',
    )
    await state.set_state(FSMDeliveryAdmin.waiting_time)


@router.message(FSMDeliveryAdmin.waiting_price)
async def process_waiting_district_name(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Произошла ошибка. Пожалуйста пришлите время доставки, время укажите в минутах (например, если доставка 1 час 30 минут, отправьте число: 90)',
    )


@router.message(FSMDeliveryAdmin.waiting_time, F.text.isdigit())
async def process_waiting_description(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(delivery_time=int(message.text))
    data = await state.get_data()
    district_data = await delivery_utils.create_data_district(data)
    await delivery_db.db_create_new_district(data=district_data)
    await state.clear()
    await process_edit_delivery_message(
        message=message,
    )
