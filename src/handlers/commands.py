from aiogram.types import Message


async def get_my_id(message: Message):
    await message.answer(text=str(message.chat.id))
