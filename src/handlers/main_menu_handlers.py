from aiogram import Router, F, types

from src.lexicons import text_main_menu_en, text_main_menu_ru
from src.keyboards import common_kb, main_kb, account_kb


router = Router(name=__name__)


@router.callback_query(F.data == 'press_location')
async def press_get_location(callback: types.CallbackQuery):
    await callback.message.answer_location(
        latitude=15.619741,
        longitude=73.737056,
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


@router.callback_query(F.data == 'press_contact')
async def get_contact(callback: types.CallbackQuery):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['contact'],
        disable_web_page_preview=True,
        parse_mode='HTML',
        reply_markup=common_kb.create_kb_back(
            language=callback.from_user.language_code)
    )


@router.callback_query(F.data == 'press_delivery')
async def get_delivery_info(callback: types.CallbackQuery):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['delivery'],
        reply_markup=common_kb.create_kb_back(
            language=callback.from_user.language_code)
    )


@router.callback_query(F.data == 'press_account')
async def open_personal_area(callback: types.CallbackQuery):
    # await callback.answer(
    #     text='Данный раздел в разработке, для отмены заказа свяжитесь пожалуйста с менеджером ресторана',
    #     show_alert=True
    # )
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en
    keyboard = await account_kb.create_kb_account(
        user_id=callback.message.chat.id,
        language=callback.from_user.language_code
    )
    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['personal_area'],
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'press_main_menu')
async def press_main_menu(callback: types.CallbackQuery):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['main_menu'],
        reply_markup=await main_kb.create_kb_main(
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
        text=text_main_menu.main_menu_dict['main_menu'],
        reply_markup=await main_kb.create_kb_main(
            language=callback.from_user.language_code,
            user_id=callback.message.chat.id
        )
    )
