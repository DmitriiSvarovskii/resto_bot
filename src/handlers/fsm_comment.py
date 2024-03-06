from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from src.keyboards import fsm_comment_kb as keyboard
from src.state import FSMComment, user_dict_comment
from src.lexicons import (
    get_comments_prompt_message,
    LEXICON_RU,
    LEXICON_KEYBOARDS_RU
)
from . import cart_handlers


router = Router(name=__name__)


@router.callback_query(F.data == 'press_comment')
async def process_waiting_comment(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text=get_comments_prompt_message(),
        reply_markup=keyboard.create_kb_fsm_comment()
    )
    await state.set_state(FSMComment.waiting_comment)


@router.message(F.text == LEXICON_KEYBOARDS_RU['cancel'])
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text=LEXICON_RU['comment_input_cancelled'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await cart_handlers.press_cart(
        message=message,
    )


@router.message(FSMComment.waiting_comment, F.text)
async def process_comment_sent(
    message: types.Message,
    state: FSMContext
):
    user_id = message.chat.id
    await state.update_data(order_comment=message.text)
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )

    user_dict_comment[user_id] = await state.get_data()

    await state.clear()

    await cart_handlers.press_cart(
        message=message,
    )
