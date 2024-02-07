# from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.redis import RedisStorage, Redis
# from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.keyboards import create_keyboard_fsm_comment
from src.fsm_state import FSMComment, user_dict_comment
from src.utils import update_cart_message
from src.lexicons import get_comments_prompt_message, LEXICON_RU


# storage: MemoryStorage = MemoryStorage()
# redis = Redis(host='localhost')

# storage = RedisStorage(redis=redis)

# dp = Dispatcher(storage=storage)


async def process_waiting_comment(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text=get_comments_prompt_message(),
        reply_markup=create_keyboard_fsm_comment()
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
    await update_cart_message(
        user_id=message.chat.id,
        message=message,
        comment=None,
    )


async def process_comment_sent(
    message: Message,
    state: FSMContext
):
    user_id = message.chat.id
    await state.update_data(comment=message.text)
    await message.answer(
        text=LEXICON_RU['good'],
        reply_markup=ReplyKeyboardRemove()
    )
    user_dict_comment[user_id] = await state.get_data()

    await state.clear()
    await update_cart_message(
        user_id=user_id,
        message=message,
        comment=user_dict_comment[user_id]["comment"],
    )
