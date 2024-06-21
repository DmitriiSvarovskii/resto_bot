from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMProductChangeDescription
from src.callbacks import ProductChangeDescriptionCallbackFactory
from src.lexicons import LEXICON_RU
from src.db import product_db
from src.keyboards import product_kb
from . import admin_handlers

router = Router(name=__name__)


@router.callback_query(ProductChangeDescriptionCallbackFactory.filter())
async def process_waiting_new_product_name(
    callback: types.CallbackQuery,
    callback_data: ProductChangeDescriptionCallbackFactory,
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
        text='Напишите новое описание для продукта, на русском языке',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMProductChangeDescription.description_rus)


@router.message(F.text == 'Отменить изменение')
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    await message.answer(
        text='Вы отменили изменение описания товара',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.process_edit_menu_mess(
        message=message,
        store_id=data['store_id']
    )


@router.message(FSMProductChangeDescription.description_rus, F.text)
async def process_waiting_new_description_rus(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(description_rus=message.text)
    await message.answer(
        text='Напишите новое описание товара на английском языке',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMProductChangeDescription.description_en)


@router.message(FSMProductChangeDescription.description_en, F.text)
async def process_comment_sent(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(description_en=message.text)
    data = await state.get_data()
    await product_db.db_update_product(
        store_id=data['store_id'],
        product_id=data['product_id'],
        data=data
    )
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )

    await admin_handlers.back_admin_menu(
        message=message,
        store_id=data['store_id']
    )

    await state.clear()
