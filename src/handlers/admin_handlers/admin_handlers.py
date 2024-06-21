from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import admin_kb, report_kb
from src.utils import report_utils
# from src.db import store_db
from src.callbacks import StoreAdminCbData


router = Router(name=__name__)


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'admin'))
async def press_admin_menu(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    message_text = 'Главное админ-меню.\nВыберите необходимый пункт'
    await callback.message.edit_text(
        text=message_text,
        reply_markup=admin_kb.create_kb_admin_main(callback_data.store_id)
    )


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'employees'))
async def press_employees(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    await callback.answer(
        text='В настоящий момент данный раздер в разработке',
        show_alert=True
    )


async def back_admin_menu(
    message: types.Message,
    store_id: int
):
    message_text = 'Главное админ-меню.\nВыберите необходимый пункт'
    await message.answer(
        text=message_text,
        reply_markup=admin_kb.create_kb_admin_main(store_id=store_id)
    )


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'stop-list'))
async def press_stop_list(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    try:
        message_text = await report_utils.create_text_stop_list(
            store_id=callback_data.store_id
        )
        if message_text is None:
            message_text = 'Стоп лист отсутствует'
        await callback.message.edit_text(
            text=message_text,
            reply_markup=admin_kb.create_kb_admin_main(
                store_id=callback_data.store_id
            )
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'edit-menu'))
async def process_edit_menu(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    await callback.message.edit_text(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_menu(
            store_id=callback_data.store_id
        )
    )


async def process_edit_menu_mess(
    message: types.Message,
    store_id: int
):
    await message.answer(
        text="Выберите необходимый пункт",
        reply_markup=admin_kb.create_kb_edit_menu(store_id=store_id)
    )


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'reports'))
async def process_reports(
    callback: types.CallbackQuery,
    callback_data: StoreAdminCbData
):
    await callback.message.edit_text(
        text="Выберите необходимый отчёт",
        reply_markup=report_kb.create_kb_report(
            store_id=callback_data.store_id)
    )


# @router.callback_query(F.data == 'press_edit_hours')
# async def process_edit_hours(callback: types.CallbackQuery):
#     await callback.message.edit_text(
#         text="message_text",
#         reply_markup=admin_kb.create_kb_admin_main()
#     )
