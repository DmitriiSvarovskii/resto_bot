from datetime import datetime
from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import report_kb
from src.utils import report_utils
from src.callbacks import StoreAdminCbData


router = Router(name=__name__)


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'sales-today'))
async def process_sales_today(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        message = await report_utils.custom_summary_text(
            store_id=callback_data.store_id,
            start_date=today,
            end_date=today
        )

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report(
                store_id=callback_data.store_id
            )
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )



@router.callback_query(F.data == 'press_sales_period')
async def process_sales_period(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )


async def process_sales_period_custom(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )

MAX_MESSAGE_LENGTH = 4096  # Максимальная длина сообщения в Telegram


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'pending-orders'))
async def process_pending_orders(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    try:
        message = await report_utils.generate_pending_orders_text(
            store_id=callback_data.store_id
        )

        if len(message) <= MAX_MESSAGE_LENGTH:
            # Если сообщение укладывается в лимит, редактируем его как обычно
            await callback.message.edit_text(
                text=message,
                reply_markup=report_kb.create_kb_report(
                    store_id=callback_data.store_id
                )
            )
        else:
            # Разбиваем сообщение на две части
            part1, part2 = split_message(message, MAX_MESSAGE_LENGTH)

            # Редактируем исходное сообщение первой частью
            await callback.message.edit_text(
                text=part1,
                reply_markup=None
            )

            # Отправляем вторую часть как новое сообщение
            await callback.message.answer(
                text=part2,
                reply_markup=report_kb.create_kb_report(
                    store_id=callback_data.store_id
                )
            )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
            show_alert=True  # Опционально: показывает всплывающее уведомление
        )


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


@router.callback_query(F.data == 'press_delivery_report')
async def process_delivery_report(callback: types.CallbackQuery):
    try:
        message = await report_utils.generate_delivery_report_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )
