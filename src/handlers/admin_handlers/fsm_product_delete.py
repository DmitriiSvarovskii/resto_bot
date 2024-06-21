from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMProductDelete
from src.callbacks import (
    ProductDeleteCallbackFactory,
)
from src.lexicons import LEXICON_RU
from src.db import product_db
from src.keyboards import product_kb, admin_kb


router = Router(name=__name__)


@router.callback_query(ProductDeleteCallbackFactory.filter())
async def process_waiting_new_product_name(
    callback: types.CallbackQuery,
    callback_data: ProductDeleteCallbackFactory,
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
    data = await state.get_data()
    await callback.message.answer(
        text='Вы отменили удаление товара',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.message.answer(
        text='Главное админ-меню.\nВыберите необходимый пункт',
        reply_markup=admin_kb.create_kb_admin_main(store_id=data['store_id'])
    )

    await state.clear()


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
        store_id=data['store_id'],
        product_id=data['product_id']
    )

    message_text = 'Главное админ-меню.\nВыберите необходимый пункт'
    await callback.message.edit_text(
        text=message_text,
        reply_markup=admin_kb.create_kb_admin_main(data['store_id'])
    )

    await state.clear()
