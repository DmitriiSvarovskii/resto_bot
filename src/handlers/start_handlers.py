from aiogram import Router, types

from src.keyboards import main_kb
from src.lexicons import LEXICON_RU
from src.db import customer_db
from src.utils import customer_utils

from aiogram.filters import CommandStart

router = Router(name=__name__)


@router.message(CommandStart())
async def process_start_command(message: types.Message):
    customer_data = await customer_utils.create_customer_data_from_message(
        message=message
    )
    await customer_db.add_new_user_to_database(
        customer_data=customer_data
    )

    keyboard = await main_kb.create_kb_main(message.chat.id)

    await message.answer(
        text=LEXICON_RU['start'],
        reply_markup=keyboard
    )
