# from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.keyboards import create_keyboard_report
from src.fsm_state import FSMSalesPeriodCustom, admin_check_order
from src.utils import update_cart_message, generate_custom_sales_summary_text
from src.lexicons import LEXICON_RU


storage: MemoryStorage = MemoryStorage()
# redis = Redis(host='localhost')

# storage = RedisStorage(redis=redis)

# dp = Dispatcher(storage=storage)


async def process_sales_period_custom(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text="Начало отчёта",
    )
    await state.set_state(FSMSalesPeriodCustom.start_date)


async def process_waiting_start_date(
    message: Message,
    state: FSMContext,
):
    await state.update_data(start_date=message.text)

    await message.answer(
        text="Конец отчёта",
    )
    await state.set_state(FSMSalesPeriodCustom.end_date)


async def process_waiting_end_date(
    message: Message,
    state: FSMContext
):
    user_id = message.chat.id

    await state.update_data(end_date=message.text)

    admin_check_order[user_id] = await state.get_data()

    text = await generate_custom_sales_summary_text(
        start_date=admin_check_order[user_id]["start_date"],
        end_date=admin_check_order[user_id]["end_date"],
    )

    await state.clear()

    await message.answer(
        text=text,
        reply_markup=create_keyboard_report()
    )


# Доделать
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
