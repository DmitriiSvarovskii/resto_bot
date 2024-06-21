from src.utils import report_utils
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.keyboards import report_kb
from src.state import FSMCheckOrder
from src.lexicons import LEXICON_RU


router = Router(name=__name__)


@router.callback_query(F.data == 'press_view_order')
async def process_view_order(
    callback: types.CallbackQuery,
    state: FSMContext
):
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text='Отправьте номер заказа, который хотите посмотреть.',
    )
    await state.set_state(FSMCheckOrder.order_id)


async def process_cancel_command_state_order(
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


@router.message(FSMCheckOrder.order_id, F.text)
async def process_waiting_order_id(message: types.Message, state: FSMContext):
    await state.update_data(order_id=int(message.text))

    data = await state.get_data()
    text = await report_utils.generate_view_order_text(data)

    await message.answer(
        text=text,
        reply_markup=report_kb.create_kb_report()
    )

    await state.clear()
