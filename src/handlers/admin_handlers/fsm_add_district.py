from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.db import delivery_db
from src.keyboards import (
    admin_kb,
)
from src.schemas import delivery_schemas
from .change_delivery_base import process_edit_delivery_message
from src.state import FSMDeliveryAdmin
from src.callbacks import StoreAdminCbData


router = Router(name=__name__)


@router.callback_query(
    StoreAdminCbData.filter(F.type_press == 'add-new-district')
)
async def process_add_new_district(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData,
    state: FSMContext
):
    await state.update_data(
        store_id=callback_data.store_id
    )
    await callback.message.answer(
        text='Введите название нового района доставки на русском языке',
    )
    await state.set_state(FSMDeliveryAdmin.waiting_name_rus)


@router.message(F.text == 'отменить')
async def process_cancel_command_state_order(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()

    await message.answer(
        text='Вы отменили добавление нового района доставки',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(
        text='Выберите пункт меню',
        reply_markup=admin_kb.create_kb_edit_menu(
            store_id=data['store_id'])
    )

    await state.clear()


@router.message(FSMDeliveryAdmin.waiting_name_rus, F.text)
async def process_waiting_name_rus(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(
        name_rus=message.text
    )
    await message.answer(
        text='Введите название нового района доставки на английском языке',
    )
    await state.set_state(FSMDeliveryAdmin.waiting_name_en)


@router.message(FSMDeliveryAdmin.waiting_name_en, F.text)
async def process_waiting_name_en(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(
        name_en=message.text
    )
    await message.answer(
        text='Введите стоимость доставки в этот район',
    )
    await state.set_state(FSMDeliveryAdmin.waiting_price)


@router.message(FSMDeliveryAdmin.waiting_name_en)
async def process_waiting_district_name(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text=(
            'Произошла ошибка. Пожалуйста пришлите цену доставки. Цену '
            'укажите цифрами, без дополнительных знаков и символов'
        ),
    )


@router.message(FSMDeliveryAdmin.waiting_price, F.text.isdigit())
async def process_waiting_district_name3(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(price=int(message.text))
    await message.answer(
        text=(
            'Введите время доставки (укажите время доставки с момента, когда '
            'курьеру передели заказ, время укажите в минутах.)'
        ),
    )
    await state.set_state(FSMDeliveryAdmin.waiting_time)


@router.message(FSMDeliveryAdmin.waiting_price)
async def process_waiting_district_name2(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text=(
            'Произошла ошибка. Пожалуйста пришлите время доставки, время '
            'укажите в минутах (например, если доставка 1 час 30 минут, '
            'отправьте число: 90)'
        ),
    )


@router.message(FSMDeliveryAdmin.waiting_time, F.text.isdigit())
async def process_waiting_description(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(delivery_time=int(message.text))

    data = await state.get_data()
    district_data = delivery_schemas.CreateDelivery(**data)
    await delivery_db.db_create_new_district(data=district_data)

    await process_edit_delivery_message(
        message=message,
        store_id=data['store_id']
    )

    await state.clear()
