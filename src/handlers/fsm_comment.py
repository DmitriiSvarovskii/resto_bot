from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from src.keyboards import fsm_comment_kb as keyboard
from src.state import FSMComment, user_dict_comment
from src.lexicons import (
    text_comment_ru,
    text_comment_en,
    text_common_ru,
    text_common_en,
)
from . import cart_handlers


router = Router(name=__name__)


@router.callback_query(F.data == 'press_comment')
async def process_waiting_comment(
    callback: types.CallbackQuery,
    state: FSMContext
):

    text_comment = (text_comment_ru
                    if callback.from_user.language_code == 'ru'
                    else text_comment_en)
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text=text_comment.create_comments_message(),
        reply_markup=keyboard.create_kb_fsm_comment(
            language=callback.from_user.language_code
        )
    )
    await state.set_state(FSMComment.waiting_comment)


@router.message(
    lambda x: x.text == text_common_en.common_dict['cancel'] or
    x.text == text_common_ru.common_dict['cancel'],
    ~StateFilter(default_state)
)
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    text_comment = (text_comment_ru
                    if message.from_user.language_code == 'ru'
                    else text_comment_en)
    await message.answer(
        text=text_comment.comment_dict['comment_input_cancelled'],
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
    text_common = (text_common_ru
                   if message.from_user.language_code == 'ru'
                   else text_common_en)
    user_id = message.chat.id
    await state.update_data(order_comment=message.text)
    await message.answer(
        text=text_common.common_dict['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )

    user_dict_comment[user_id] = await state.get_data()

    await state.clear()

    await cart_handlers.press_cart(
        message=message,
    )
