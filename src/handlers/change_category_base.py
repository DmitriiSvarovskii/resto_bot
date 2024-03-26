from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import category_kb
from src.db import category_db
from src.callbacks import (
    CategoryChangeCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_change_category')
async def process_change_category(callback: types.CallbackQuery):
    categories = await category_db.get_all_categories()
    keyboard = await category_kb.create_kb_category_admin(
        categories=categories,
        callback_data=CategoryChangeCallbackFactory,
        language=callback.from_user.language_code
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


@router.callback_query(CategoryChangeCallbackFactory.filter())
async def get_admin_change_avail_category(
    callback: types.CallbackQuery,
    callback_data: CategoryChangeCallbackFactory
):
    try:
        keyboard = await category_kb.create_kb_change_category(
            category_id=callback_data.category_id
        )
        await callback.message.edit_text(text='Выберите необходимый пункт',
                                         reply_markup=keyboard)
        await callback.answer(text='Ок')
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )
