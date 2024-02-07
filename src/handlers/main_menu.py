from aiogram.types import CallbackQuery

from src.lexicons import LEXICON_RU
from src.keyboards import (
    create_keyboard_del,
    create_keyboard_back,
    create_keyboard_main
)


async def press_get_location(callback: CallbackQuery):
    await callback.message.answer_location(
        latitude=15.619741,
        longitude=73.737056,
        reply_markup=create_keyboard_del()
    )


async def press_del_location(callback: CallbackQuery):
    await callback.message.delete()


async def get_contact(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['contact'],
        parse_mode='HTML',
        reply_markup=create_keyboard_back()
    )


async def get_delivery_info(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['delivery'],
        reply_markup=create_keyboard_back()
    )


# async def open_personal_area(callback: CallbackQuery):
#     # keyboard = await personal_area(callback.message.chat.id)
#     await callback.message.edit_text(
#         text=LEXICON_RU['personal_area'],
#         reply_markup=keyboard.as_markup()
#     )

async def press_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['main_menu'],
        reply_markup=await create_keyboard_main(callback.message.chat.id)
    )


async def press_back_main_menu(callback: CallbackQuery):
    await callback.message.answer(
        text=LEXICON_RU['main_menu'],
        reply_markup=await create_keyboard_main(callback.message.chat.id)
    )
