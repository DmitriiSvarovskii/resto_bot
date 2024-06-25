from aiogram import Router, F, types

from src.lexicons import text_main_menu_en, text_main_menu_ru
from src.keyboards import common_kb, main_kb, account_kb
from src.callbacks import StoreMenuCbData
from src.db import store_db, delivery_db


router = Router(name=__name__)


@router.callback_query(StoreMenuCbData.filter(F.type == 'location'))
async def press_get_location(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    data = await store_db.get_store_info(
        store_id=callback_data.store_id
    )

    await callback.message.answer_location(
        latitude=data.latitude,
        longitude=data.longitude,
        reply_markup=common_kb.create_kb_del(
            language=callback.from_user.language_code
        )
    )


@router.callback_query(F.data == 'press_del')
async def press_del_location(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)


@router.callback_query(StoreMenuCbData.filter(F.type == 'contact'))
async def get_contact(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['contact'],
        disable_web_page_preview=True,
        parse_mode='HTML',
        reply_markup=common_kb.create_kb_back(
            language=callback.from_user.language_code,
            store_id=callback_data.store_id
        )
    )


@router.callback_query(StoreMenuCbData.filter(F.type == 'delivery'))
async def get_delivery_info(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    data = await delivery_db.get_delivery_districts(
        store_id=callback_data.store_id
    )
    if callback.from_user.language_code == 'ru':
        text_info_delivery = text_main_menu_ru.create_delivery_info(data)
    else:
        text_info_delivery = text_main_menu_en.create_delivery_info(data)

    await callback.message.edit_text(
        text=text_info_delivery,
        reply_markup=common_kb.create_kb_back(
            language=callback.from_user.language_code,
            store_id=callback_data.store_id
        )
    )


@router.callback_query(StoreMenuCbData.filter(F.type == 'account'))
async def open_personal_area(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en
    keyboard = await account_kb.create_kb_account(
        user_id=callback.message.chat.id,
        language=callback.from_user.language_code,
        store_id=callback_data.store_id
    )
    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['personal_area'],
        reply_markup=keyboard
    )


@router.callback_query(StoreMenuCbData.filter(F.type == 'main-menu'))
async def press_main_menu(
    callback: types.CallbackQuery,
    callback_data: StoreMenuCbData
):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['start'],
        reply_markup=await main_kb.create_kb_main(
            store_id=callback_data.store_id,
            language=callback.from_user.language_code,
            user_id=callback.message.chat.id
        )
    )


@router.callback_query(F.data == 'press_back_main_menu')
async def press_back_main_menu(callback: types.CallbackQuery):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    await callback.message.answer(
        text=text_main_menu.main_menu_dict['start'],
        reply_markup=await main_kb.create_kb_main(
            language=callback.from_user.language_code,
            user_id=callback.message.chat.id
        )
    )
