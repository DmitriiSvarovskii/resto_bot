from aiogram.types import Message

from src.keyboards import create_keyboard_main
from src.lexicons import LEXICON_RU
from src.db import customer_db
from src.utils_new import customer_utils


async def process_start_command(message: Message):
    customer_data = await customer_utils.create_customer_data_from_message(
        message=message
    )

    await customer_db.add_new_user_to_database(
        customer_data=customer_data
    )

    keyboard = await create_keyboard_main(message.chat.id)

    await message.answer(
        text=LEXICON_RU['start'],
        reply_markup=keyboard
    )
