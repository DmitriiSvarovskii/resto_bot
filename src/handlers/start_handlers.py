from aiogram.types import Message

from src.keyboards import main_keyboards
from src.lexicons import LEXICON_RU
from src.db import customer_db
from src.utils import customer_utils, create_qr


async def process_start_command(message: Message):
    customer_data = await customer_utils.create_customer_data_from_message(
        message=message
    )
    await customer_db.add_new_user_to_database(
        customer_data=customer_data
    )

    keyboard = await main_keyboards.create_keyboard_main(message.chat.id)
    # img = await create_qr.generate_qr_code()

    # await message.answer_photo(
    #     photo=await create_qr.generate_qr_code(),
    # )

    await message.answer(
        text=LEXICON_RU['start'],
        reply_markup=keyboard
    )
