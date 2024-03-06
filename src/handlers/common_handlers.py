from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from src.lexicons import LEXICON_RU


router = Router(name=__name__)


@router.callback_query(F.data == 'press_pass')
async def process_pass(
    callback: CallbackQuery,
):
    await callback.answer(
        text=LEXICON_RU['invalid_request_message']
    )


async def send_echo(message: Message):
    try:
        pass
    except TypeError:
        pass
