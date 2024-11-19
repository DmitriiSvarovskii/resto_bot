from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from src.keyboards import report_kb
from src.state import FSMSalesPeriodCustom
from src.utils import report_utils
from src.lexicons import LEXICON_RU
from src.callbacks import StoreAdminCbData


router = Router(name=__name__)


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'sales-period'))
async def process_sales_period_custom(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData,
    state: FSMContext
):
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await state.update_data(store_id=callback_data.store_id)
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


MAX_MESSAGE_LENGTH = 4096


def split_message(message: str, max_length: int):
    """
    Разбивает длинное сообщение на две части по максимально допустимой длине.
    Попытка разрезать по последнему переносу строки или пробелу перед пределом.
    Если не удается, просто разрезает строго по max_length.
    """
    if len(message) <= max_length:
        return message, ''

    # Ищем место для разреза
    split_pos = message.rfind('\n', 0, max_length)
    if split_pos == -1:
        split_pos = message.rfind(' ', 0, max_length)

    if split_pos == -1:
        # Если нет подходящего места для разреза, разрезаем строго по max_length
        return message[:max_length], message[max_length:]
    else:
        return message[:split_pos], message[split_pos:].lstrip()


@router.message(FSMSalesPeriodCustom.end_date, F.text)
async def process_waiting_end_date(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(end_date=message.text)

    data = await state.get_data()

    text = await report_utils.custom_summary_text(
        store_id=data["store_id"],
        start_date=data["start_date"],
        end_date=data["end_date"],
    )

    if len(text) <= MAX_MESSAGE_LENGTH:
        # Если сообщение укладывается в лимит, редактируем его как обычно
        await message.answer(
            text=text,
            reply_markup=report_kb.create_kb_report(store_id=data["store_id"])
        )
    else:
        part1, part2 = split_message(text, MAX_MESSAGE_LENGTH)

        await message.answer(
            text=part1,
            reply_markup=None
        )

        await message.answer(
            text=part2,
            reply_markup=report_kb.create_kb_report(store_id=data["store_id"])
        )

    await state.clear()


async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    await message.answer(
        text=LEXICON_RU['comment_input_cancelled'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(
        text='Запрос отчёта отменён.',
        reply_markup=report_kb.create_kb_report(store_id=data["store_id"])
    )
    await state.clear()
