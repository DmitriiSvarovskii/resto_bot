from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.keyboards import fsm_comment_keyboards as keyboard
from src.fsm_state import FSMComment, user_dict_comment
from src.lexicons import get_comments_prompt_message, LEXICON_RU
from . import cart_handlers


async def process_waiting_comment(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text=get_comments_prompt_message(),
        reply_markup=keyboard.create_keyboard_fsm_comment()
    )
    await state.set_state(FSMComment.waiting_comment)


async def process_cancel_command_state(
    message: Message,
    state: FSMContext
):
    await message.answer(
        text=LEXICON_RU['comment_input_cancelled'],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    await cart_handlers.press_cart(
        message=message,
    )


async def process_comment_sent(
    message: Message,
    state: FSMContext
):
    user_id = message.chat.id
    await state.update_data(order_comment=message.text)
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=ReplyKeyboardRemove()
    )
    user_dict_comment[user_id] = await state.get_data()

    await state.clear()

    await cart_handlers.press_cart(
        message=message,
    )
