from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.keyboards import fsm_qr_code_kb as keyboard
from src.state import FSMQrCode
from src.lexicons import LEXICON_RU, LEXICON_KEYBOARDS_RU
from src.utils import create_qr
from . import admin_handlers


router = Router(name=__name__)


@router.callback_query(F.data == 'press_qr_code')
async def process_waiting_link(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text='Пришлите ссылку для генерации в qr-code',
        reply_markup=keyboard.create_kb_fsm_qr_code()
    )
    await state.set_state(FSMQrCode.waiting_link)


@router.message(F.text == LEXICON_KEYBOARDS_RU['cancel_qr'])
async def process_cancel_create_qr_state(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text=LEXICON_RU['link_input_cancelled'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.back_admin_menu(
        message=message
    )


@router.message(FSMQrCode.waiting_link, F.text)
async def process_create_qr_code(
    message: types.Message,
    state: FSMContext
):
    await message.answer_photo(
        photo=await create_qr.generate_qr_code(message.text),
    )

    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()

    await admin_handlers.back_admin_menu(
        message=message
    )
