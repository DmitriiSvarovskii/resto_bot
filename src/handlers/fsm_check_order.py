from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.keyboards import report_keyboards
from src.fsm_state import FSMCheckOrder, admin_check_order
from src.lexicons import LEXICON_RU
from src.utils import report_utils


async def process_view_order(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text='Отправьте номер заказа, который хотите посмотреть.',
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
    await message.answer(
        text='Запрос отчёта отменён.',
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_waiting_order_id(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.update_data(order_id=int(message.text))

    admin_check_order[user_id] = await state.get_data()

    await state.clear()

    text = await report_utils.generate_view_order_text(
        admin_check_order[user_id]['order_id']
    )

    await message.answer(
        text=text,
        reply_markup=report_keyboards.create_keyboard_report()
    )
