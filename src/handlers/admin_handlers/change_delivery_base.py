from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import admin_kb, report_kb
from src.utils import report_utils
# from src.db import store_db
from src.callbacks import StoreAdminCbData


router = Router(name=__name__)


@router.callback_query(
    StoreAdminCbData.filter(F.type_press == 'edit-delivery')
)
async def process_edit_delivery(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    await callback.message.edit_text(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_delivery(
            store_id=callback_data.store_id
        )
    )


async def process_edit_delivery_message(
    message: types.Message,
    store_id: int
):
    await message.answer(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_delivery(store_id=store_id)
    )
