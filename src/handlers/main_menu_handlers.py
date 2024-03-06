from aiogram import Router, F, types

from src.lexicons import LEXICON_RU
from src.keyboards import common_kb, main_kb


router = Router(name=__name__)


@router.callback_query(F.data == 'press_location')
async def press_get_location(callback: types.CallbackQuery):
    await callback.message.answer_location(
        latitude=15.619741,
        longitude=73.737056,
        reply_markup=common_kb.create_kb_del()
    )


@router.callback_query(F.data == 'press_del')
async def press_del_location(callback: types.CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == 'press_contact')
async def get_contact(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['contact'],
        disable_web_page_preview=True,
        parse_mode='HTML',
        reply_markup=common_kb.create_kb_back(),

    )


@router.callback_query(F.data == 'press_delivery')
async def get_delivery_info(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['delivery'],
        reply_markup=common_kb.create_kb_back()
    )


@router.callback_query(F.data == 'press_account')
async def open_personal_area(callback: types.CallbackQuery):
    pass
    # keyboard = await personal_area(callback.message.chat.id)
    # await callback.message.edit_text(
    #     text=LEXICON_RU['personal_area'],
    #     reply_markup=keyboard.as_markup()
    # )


@router.callback_query(F.data == 'press_main_menu')
async def press_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['main_menu'],
        reply_markup=await main_kb.create_kb_main(
            callback.message.chat.id
        )
    )


@router.callback_query(F.data == 'press_back_main_menu')
async def press_back_main_menu(callback: types.CallbackQuery):
    await callback.message.answer(
        text=LEXICON_RU['main_menu'],
        reply_markup=await main_kb.create_kb_main(
            callback.message.chat.id
        )
    )
