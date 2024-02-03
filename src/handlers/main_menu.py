from aiogram.types import CallbackQuery

from src.lexicons import LEXICON_RU
from src.keyboards import (
    create_keyboard_del,
    create_keyboard_back,
    create_keyboard_main
)
from src.database import get_async_session
from src.crud import crud_get_daily_sales, get_user_info


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


# async def press_test(callback: CallbackQuery):
    # async for session in get_async_session():
    #     product = await crud_get_daily_sales(

    #         session=session
    #     )
    #     product2 = await crud_get_daily_sales(
    #         filter=67,
    #         session=session
    #     )
    #     product3 = await crud_get_daily_sales(
    #         start_date="2024-01-29",
    #         end_date='2024-01-30',
    #         session=session
    #     )
    #     product4 = await crud_get_daily_sales(
    #         start_date="2024-01-29",
    #         session=session
    #     )
    #     product5 = await crud_get_daily_sales(
    #         start_date="2024-01-29",
    #         end_date="2024-01-29",
    #         session=session
    #     )
    #     product6 = await crud_get_daily_sales(
    #         canceled='Отменён',
    #         session=session
    #     )
    #     user = await get_user_info(
    #         resourse='table_3',
    #         session=session
    #     )
    #     user2 = await get_user_info(
    #         user_id=606825877,
    #         session=session
    #     )
    #     break
#     await callback.answer(text='test press')
