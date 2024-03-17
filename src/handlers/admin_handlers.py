from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import admin_kb, report_kb
from src.utils import report_utils
# from src.db import store_db


router = Router(name=__name__)


@router.callback_query(F.data == 'press_admin')
async def press_admin_menu(callback: types.CallbackQuery):
    message_text = 'Главное админ-меню.\nВыберите необходимый пункт'
    await callback.message.edit_text(
        text=message_text,
        reply_markup=admin_kb.create_kb_admin_main()
    )


@router.callback_query(F.data == 'press_employees')
async def press_employees(callback: types.CallbackQuery):
    await callback.answer(
        text='В настоящий момент данный раздер в разработке',
        show_alert=True
    )


async def back_admin_menu(message: types.Message):
    message_text = 'Главное админ-меню.\nВыберите необходимый пункт'
    await message.answer(
        text=message_text,
        reply_markup=admin_kb.create_kb_admin_main()
    )


@router.callback_query(F.data == 'press_stop_list')
async def press_stop_list(callback: types.CallbackQuery):
    try:
        message_text = await report_utils.create_text_stop_list()
        if message_text is None:
            message_text = 'Стоп лист отсутствует'
        await callback.message.edit_text(
            text=message_text,
            reply_markup=admin_kb.create_kb_admin_main()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


@router.callback_query(F.data == 'press_edit_menu')
async def process_edit_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_menu()
    )


async def process_edit_menu_mess(message: types.Message):
    await message.answer(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_menu()
    )


@router.callback_query(F.data == 'press_reports')
async def process_reports(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="Выберите необходимый отчёт",
        reply_markup=report_kb.create_kb_report()
    )


# @router.callback_query(F.data == 'press_edit_hours')
# async def process_edit_hours(callback: types.CallbackQuery):
#     await callback.message.edit_text(
#         text="message_text",
#         reply_markup=admin_kb.create_kb_admin_main()
#     )
