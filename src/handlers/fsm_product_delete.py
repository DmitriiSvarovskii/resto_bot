from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMProductDelete
from src.callbacks import (
    ProductDeleteCallbackFactory,
)
from src.lexicons import LEXICON_RU
from src.db import product_db
from src.keyboards import product_kb
from src.handlers import admin_handlers

router = Router(name=__name__)


@router.callback_query(ProductDeleteCallbackFactory.filter())
async def process_waiting_new_product_name(
    callback: types.CallbackQuery,
    callback_data: ProductDeleteCallbackFactory,
    state: FSMContext
):
    await state.update_data(product_id=callback_data.product_id)
    await callback.message.delete()
    keyboard = await product_kb.create_kb_product_delete()
    await callback.message.answer(
        text=('Вы действительно хотите удалить товар? Удаленный товар '
              'не подлежит восстановлению'),
        reply_markup=keyboard
    )
    await state.set_state(FSMProductDelete.confirmation)


@router.callback_query(
    FSMProductDelete.confirmation,
    F.data == 'press_cancel_delete'
)
async def process_cancel_command_state(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.answer(
        text='Вы отменили удаление товара',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.process_edit_menu_mess(
        callback=callback,
    )


@router.callback_query(
    FSMProductDelete.confirmation,
    F.data == 'press_approval_delete'
)
async def process_comment_sent(
    callback: types.CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()
    await callback.message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await product_db.db_change_delete_flag_product(
        product_id=data['product_id']
    )
    await state.clear()

    await admin_handlers.press_admin_menu(
        callback=callback,
    )
