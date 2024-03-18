from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import admin_kb, report_kb
from src.utils import report_utils
# from src.db import store_db


router = Router(name=__name__)


@router.callback_query(F.data == 'press_edit_delivery')
async def process_edit_delivery(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_delivery()
    )


async def process_edit_delivery_message(message: types.Message):
    await message.answer(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_delivery()
    )
