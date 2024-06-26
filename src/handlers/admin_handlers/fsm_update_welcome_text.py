from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMStore
from src.callbacks import StoreCbData
from src.lexicons import LEXICON_RU
from src.db import store_db
from src.keyboards import product_kb
from . import admin_handlers

router = Router(name=__name__)


@router.callback_query(StoreCbData.filter(F.type_update == 'welcome-text'))
async def process_waiting_new_welcome_text(
    callback: types.CallbackQuery,
    callback_data: StoreCbData,
    state: FSMContext
):
    await state.update_data(store_id=callback_data.store_id)
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text='Пришлите новый текст-приветсвие',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    await state.set_state(FSMStore.waiting_welcome_text)


@router.message(F.text == 'Отменить изменение')
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    await message.answer(
        text='Вы отменили изменение текста-приветствия',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.process_edit_menu_mess(
        message=message,
        store_id=data['store_id']
    )


@router.message(
    FSMStore.waiting_welcome_text, F.text)
async def process_welcome_text_sent(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    update_values = {
        'welcome_message': message.text,
    }
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await store_db.db_update_store(
        store_id=data['store_id'],
        update_values=update_values
    )
    await admin_handlers.back_admin_menu(
        message=message,
    )

    await state.clear()
