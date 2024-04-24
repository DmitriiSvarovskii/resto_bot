from aiogram import Router, F, types
from aiogram.filters import Command

from src.lexicons import text_common_ru, text_common_en


router = Router(name=__name__)


@router.callback_query(F.data == 'press_pass')
async def process_pass(
    callback: types.CallbackQuery,
):
    text_common = (text_common_ru
                   if callback.from_user.language_code == 'ru'
                   else text_common_en)
    await callback.answer(
        text=text_common.common_dict['invalid_request']
    )


# @router.message()
# async def send_echo(message: types.Message):
#     try:
#         if message.text or message.voice:
#             await message.delete()
#     except TypeError:
#         pass


@router.message(Command('id'))
async def get_my_id(message: types.Message):
    text_common = (text_common_ru
                   if message.from_user.language_code == 'ru'
                   else text_common_en)

    await message.answer(
        text=text_common.get_telegram_id(
            user_id=message.chat.id
        )
    )
