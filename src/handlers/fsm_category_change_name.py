from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMCategoryChangeName
from src.callbacks import CategoryChangeNameCallbackFactory
from src.lexicons import LEXICON_RU
from src.db import category_db
from src.keyboards import product_kb
from src.handlers import admin_handlers

router = Router(name=__name__)


@router.callback_query(CategoryChangeNameCallbackFactory.filter())
async def process_waiting_new_category_name(
    callback: types.CallbackQuery,
    callback_data: CategoryChangeNameCallbackFactory,
    state: FSMContext
):
    await state.update_data(category_id=callback_data.category_id)
    await callback.message.delete()
    await callback.message.answer(
        text='Напишите новое имя для продукта',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMCategoryChangeName.name)


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


@router.message(FSMCategoryChangeName.name, F.text)
async def process_comment_sent(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await category_db.db_update_category_name(
        category_id=data['category_id'],
        category_name=message.text,
    )
    await state.clear()

    await admin_handlers.back_admin_menu(
        message=message,
    )
