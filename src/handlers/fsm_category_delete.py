from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMCategoryDelete
from src.callbacks import (
    CategoryDeleteCallbackFactory,
)
from src.lexicons import LEXICON_RU
from src.db import category_db
from src.keyboards import category_kb
from src.handlers import admin_handlers

router = Router(name=__name__)


@router.callback_query(CategoryDeleteCallbackFactory.filter())
async def process_waiting_new_category_name(
    callback: types.CallbackQuery,
    callback_data: CategoryDeleteCallbackFactory,
    state: FSMContext
):
    await state.update_data(category_id=callback_data.category_id)
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    keyboard = await category_kb.create_kb_category_delete()
    await callback.message.answer(
        text=('Вы действительно хотите удалить товар? Удаленный товар '
              'не подлежит восстановлению'),
        reply_markup=keyboard
    )
    await state.set_state(FSMCategoryDelete.confirmation)


@router.callback_query(
    FSMCategoryDelete.confirmation,
    F.data == 'press_cancel_delete_category'
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
    await admin_handlers.press_admin_menu(
        callback=callback,
    )


@router.callback_query(
    FSMCategoryDelete.confirmation,
    F.data == 'press_approval_delete_category'
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
    await category_db.db_change_delete_flag_category(
        category_id=data['category_id']
    )
    await state.clear()

    await admin_handlers.press_admin_menu(
        callback=callback,
    )
