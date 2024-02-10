from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.keyboards import report_keyboards
from src.fsm_state import FSMSalesPeriodCustom, admin_check_order
from src.utils import report_utils
from src.lexicons import LEXICON_RU


async def process_sales_period_custom(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text=(
            "Укажите дату начала отчёта.\n"
            "Дату укажите в формате 2020-01-01 (гггг-мм-дд)"
        ),
    )
    await state.set_state(FSMSalesPeriodCustom.start_date)


async def process_waiting_start_date(
    message: Message,
    state: FSMContext,
):
    await state.update_data(start_date=message.text)

    await message.answer(
        text=(
            "Укажите дату конца отчёта.\n"
            "Дату укажите в формате 2020-01-01 (гггг-мм-дд)"
        ),
    )
    await state.set_state(FSMSalesPeriodCustom.end_date)


async def process_waiting_end_date(
    message: Message,
    state: FSMContext
):
    user_id = message.chat.id

    await state.update_data(end_date=message.text)

    admin_check_order[user_id] = await state.get_data()

    text = await report_utils.custom_summary_text(
        start_date=admin_check_order[user_id]["start_date"],
        end_date=admin_check_order[user_id]["end_date"],
    )

    await state.clear()

    await message.answer(
        text=text,
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_cancel_command_state(
    message: Message,
    state: FSMContext
):
    await message.answer(
        text=LEXICON_RU['comment_input_cancelled'],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    await message.answer(
        text='Запрос отчёта отменён.',
        reply_markup=report_keyboards.create_keyboard_report()
    )
