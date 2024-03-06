from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.keyboards import report_kb
from src.state import FSMAdReport, admin_check_order
from src.utils import report_utils
from src.lexicons import LEXICON_RU, message_text


router = Router(name=__name__)


@router.callback_query(F.data == 'press_ad_report')
async def process_resourse_report(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text=message_text.report_text['resourse_fsm'],
    )
    await state.set_state(FSMAdReport.resourse)


async def process_cancel_command_state_resourse(
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


@router.message(FSMAdReport.resourse, F.text)
async def process_waiting_resourser(
    message: types.Message,
    state: FSMContext
):
    user_id = message.chat.id
    await state.update_data(resourse=message.text)

    admin_check_order[user_id] = await state.get_data()

    await state.clear()

    text = await report_utils.generate_res_report_text(
        admin_check_order[user_id]['resourse']
    )

    await message.answer(
        text=text,
        reply_markup=report_kb.create_kb_report()
    )
