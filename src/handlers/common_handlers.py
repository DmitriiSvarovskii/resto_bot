from aiogram import Router, F, types
from aiogram.filters import Command

from src.lexicons import LEXICON_RU


router = Router(name=__name__)


@router.callback_query(F.data == 'press_pass')
async def process_pass(
    callback: types.CallbackQuery,
):
    await callback.answer(
        text=LEXICON_RU['invalid_request_message']
    )


async def send_echo(message: types.Message):
    try:
        pass
    except TypeError:
        pass


@router.message(Command('id'))
async def get_my_id(message: types.Message):
    await message.answer(text=f'Ваш id в телеграм {message.chat.id}')
