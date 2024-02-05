# from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.keyboards import create_keyboard_report
from src.fsm_state import FSMCheckOrder, admin_check_order
from src.utils import update_cart_message, generate_view_order_text
from src.lexicons import LEXICON_RU


storage: MemoryStorage = MemoryStorage()
# redis = Redis(host='localhost')

# storage = RedisStorage(redis=redis)

# dp = Dispatcher(storage=storage)


async def process_view_order(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text='Order id',
    )
    await state.set_state(FSMCheckOrder.order_id)


async def process_cancel_command_state_order(
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


async def process_waiting_order_id(
    message: Message,
    state: FSMContext
):
    user_id = message.chat.id
    await state.update_data(order_id=int(message.text))

    admin_check_order[user_id] = await state.get_data()

    await state.clear()

    text = await generate_view_order_text(
        admin_check_order[user_id]['order_id']
    )

    await message.answer(
        text=text,
        reply_markup=create_keyboard_report()
    )
