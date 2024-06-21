from datetime import datetime
from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import report_kb
from src.utils import report_utils


router = Router(name=__name__)


@router.callback_query(F.data == 'press_sales_today')
async def process_sales_today(callback: types.CallbackQuery):
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        message = await report_utils.custom_summary_text(
            start_date=today,
            end_date=today
        )

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report()
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


@router.callback_query(F.data == 'press_pending_orders')
async def process_pending_orders(callback: types.CallbackQuery):
    try:
        message = await report_utils.generate_pending_orders_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


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
