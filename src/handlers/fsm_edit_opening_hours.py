import re
from datetime import datetime

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from src.handlers import admin_handlers
from src.state import FSMOpeningHours
from src.db import store_db
from src.keyboards import fsm_edit_openong_hours_kb as kb


router = Router(name=__name__)


@router.callback_query(F.data == 'press_edit_hours')
async def process_edit_hours(
    callback: types.CallbackQuery,
    state: FSMContext
):
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text='Введите время начала работы в формате "чч:мм" (например: 14:00)',
        reply_markup=kb.create_kb_fsm_edit_openong_hours()
    )
    await state.set_state(FSMOpeningHours.opening_time)


@router.message(
    F.text == 'Отменить редактирование',
    ~StateFilter(default_state)
)
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Вы отменили изменение графика работы',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.back_admin_menu(
        message=message,
    )

time_pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')


@router.message(FSMOpeningHours.opening_time, F.text)
async def process_wait_opening_time(
    message: types.Message,
    state: FSMContext
):
    text = message.text.strip()

    if not time_pattern.match(text):
        await message.reply("Текст должен быть в формате ЧЧ:ММ (например: 14:00). Пожалуйста, введите корректное время.")
        return
    else:
        await state.update_data(opening_time=message.text)
        await message.answer(
            text='Введите время окончания работы в формате "чч:мм" (например: 23:00)',
        )
        await state.set_state(FSMOpeningHours.closing_time)


@router.message(FSMOpeningHours.closing_time, F.text)
async def process_wait_closing_time(
    message: types.Message,
    state: FSMContext
):
    text = message.text.strip()

    if not time_pattern.match(text):
        await message.reply("Текст должен быть в формате ЧЧ:ММ (например: 14:00). Пожалуйста, введите корректное время.")
        return
    else:
        await state.update_data(closing_time=message.text)
        data = await state.get_data()

        opening_time = datetime.strptime(data['opening_time'], '%H:%M').time()
        closing_time = datetime.strptime(data['closing_time'], '%H:%M').time()

        await store_db.db_update_opening_hours(
            opening_time=opening_time,
            closing_time=closing_time
        )

        await admin_handlers.back_admin_menu(
            message=message,
        )

        await state.clear()
