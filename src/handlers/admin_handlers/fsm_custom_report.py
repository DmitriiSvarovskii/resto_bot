from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from src.keyboards import report_kb
from src.state import FSMSalesPeriodCustom
from src.utils import report_utils
from src.lexicons import LEXICON_RU


router = Router(name=__name__)


@router.callback_query(F.data == 'press_sales_period_custom')
async def process_sales_period_custom(
    callback: types.CallbackQuery,
    state: FSMContext
):
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text=(
            "Укажите дату начала отчёта.\n"
            "Дату укажите в формате 2020-01-01 (гггг-мм-дд)"
        ),
    )
    await state.set_state(FSMSalesPeriodCustom.start_date)


@router.message(FSMSalesPeriodCustom.start_date, F.text)
async def process_waiting_start_date(
    message: types.Message,
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


@router.message(FSMSalesPeriodCustom.end_date, F.text)
async def process_waiting_end_date(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(end_date=message.text)

    data = await state.get_data()

    text = await report_utils.custom_summary_text(
        start_date=data["start_date"],
        end_date=data["end_date"],
    )

    await state.clear()

    await message.answer(
        text=text,
        reply_markup=report_kb.create_kb_report()
    )


async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text=LEXICON_RU['comment_input_cancelled'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await message.answer(
        text='Запрос отчёта отменён.',
        reply_markup=report_kb.create_kb_report()
    )
