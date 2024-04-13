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
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text='Напишите новое название категории на русском языке',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMCategoryChangeName.name_rus)


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


@router.message(FSMCategoryChangeName.name_rus, F.text)
async def process_waiting_new_category_name_rus(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(category_name_rus=message.text)
    await message.answer(
        text='Напишите новое название категории на английском языке',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMCategoryChangeName.name_en)


@router.message(FSMCategoryChangeName.name_en, F.text)
async def process_waiting_new_category_name_en(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(category_name_en=message.text)
    data = await state.get_data()
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await category_db.db_update_category_name(**data)
    await state.clear()

    await admin_handlers.back_admin_menu(
        message=message,
    )
