from aiogram import types, Router, F

from src.keyboards import store_kb
from src.db import store_db


router = Router(name=__name__)


@router.callback_query(F.data == 'press_toggle_bot')
async def process_toggle_bot(callback: types.CallbackQuery):
    store_info = await store_db.get_store_info()
    keyboard = store_kb.create_kb_toggle_bot(
        store_info=store_info
    )
    await callback.answer('ok')
    await callback.message.edit_text(
        text="Меню активации/деактивации бота",
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'press_toggle_working_bot')
async def process_toggle_working_bot(callback: types.CallbackQuery):
    await store_db.change_is_active_bot()

    store_info = await store_db.get_store_info()
    keyboard = store_kb.create_kb_toggle_bot(
        store_info=store_info
    )
    await callback.answer('ok')
    await callback.message.edit_reply_markup(
        text="Меню активации/деактивации бота",
        reply_markup=keyboard
    )
