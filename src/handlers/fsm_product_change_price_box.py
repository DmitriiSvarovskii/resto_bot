from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMProductChangePriceBox
from src.callbacks import ProductChangePriceBoxCallbackFactory
from src.lexicons import LEXICON_RU
from src.db import product_db
from src.keyboards import product_kb
from src.handlers import admin_handlers

router = Router(name=__name__)


@router.callback_query(ProductChangePriceBoxCallbackFactory.filter())
async def process_waiting_new_product_name(
    callback: types.CallbackQuery,
    callback_data: ProductChangePriceBoxCallbackFactory,
    state: FSMContext
):
    await state.update_data(product_id=callback_data.product_id)
    await callback.message.delete()
    await callback.message.answer(
        text='Напишите новое имя для продукта',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMProductChangePriceBox.price_box)


@router.message(F.text == 'Отменить изменение')
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Вы отменили изменение имени',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.process_edit_menu_mess(
        message=message,
    )


@router.message(FSMProductChangePriceBox.price_box, F.text.isdigit())
async def process_comment_sent(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(price_box=int(message.text))
    data = await state.get_data()
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await product_db.db_update_product(
        product_id=data['product_id'],
        data=data
    )
    await state.clear()

    await admin_handlers.back_admin_menu(
        message=message,
    )
