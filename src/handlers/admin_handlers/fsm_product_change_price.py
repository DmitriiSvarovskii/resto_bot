from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMProductChangePrice
from src.callbacks import ProductChangePriceCallbackFactory
from src.lexicons import LEXICON_RU
from src.db import product_db
from src.keyboards import product_kb
from . import admin_handlers

router = Router(name=__name__)


@router.callback_query(ProductChangePriceCallbackFactory.filter())
async def process_waiting_new_product_name(
    callback: types.CallbackQuery,
    callback_data: ProductChangePriceCallbackFactory,
    state: FSMContext
):
    await state.update_data(
        product_id=callback_data.product_id,
        store_id=callback_data.store_id
    )
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text='Напишите новую цену для продукта',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMProductChangePrice.price)


@router.message(F.text == 'Отменить изменение')
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    await message.answer(
        text='Вы отменили изменение цены',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await admin_handlers.process_edit_menu_mess(
        message=message,
        store_id=data['store_id']
    )

    await state.clear()


@router.message(FSMProductChangePrice.price, F.text.isdigit())
async def process_comment_sent(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(price=int(message.text))
    data = await state.get_data()
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await product_db.db_update_product(
        store_id=data['store_id'],
        product_id=data['product_id'],
        data=data
    )

    await admin_handlers.back_admin_menu(
        message=message,
        store_id=data['store_id']
    )

    await state.clear()


@router.message(FSMProductChangePrice.price)
async def warning_not_price(
    message: types.Message,
):
    await message.answer(
        text=(
            'Возникла ошибка при вводе цены, пожалуйста, повторите попытку. '
            'Цену указывайте только цифрами, без '
            'использования знаков, букв и тп'
        ),
    )
