from aiogram.types import Message, FSInputFile

from src.keyboards import main_keyboards
from src.lexicons import LEXICON_RU
from src.db import customer_db
from src.utils import customer_utils, create_qr
import io


async def process_start_command(message: Message):
    customer_data = await customer_utils.create_customer_data_from_message(
        message=message
    )
    await customer_db.add_new_user_to_database(
        customer_data=customer_data
    )

    keyboard = await main_keyboards.create_keyboard_main(message.chat.id)
    # img = await create_qr.generate_qr_code()
    # buffer = io.BytesIO()
    # img.save(buffer, format='PNG')  # Сохраняем изображение в буфер
    # buffer.seek(0)  # Возвращаем указатель чтения в начало буфера
    # input_file = FSInputFile(buffer)  # Создаем InputFile из буфера

    await message.answer(
        text=LEXICON_RU['start'],
        reply_markup=keyboard
    )
    # await message.answer_photo(
    #     photo=input_file
    # )
