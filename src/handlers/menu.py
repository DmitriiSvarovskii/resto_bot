from aiogram.types import CallbackQuery

from src.lexicons import LEXICON_RU
from src.database import get_async_session
from src.crud import crud_get_all_categories, crud_get_store_info
from src.keyboards import create_keyboard_category, create_keyboard_main
from src.services import is_valid_time_warning
from src.callbacks import CategoryIdCallbackFactory
from .utils import get_products_by_category, get_keyboard_products_by_category


async def get_menu_category(callback: CallbackQuery):
    if is_valid_time_warning():
        await callback.answer(
            text=LEXICON_RU['closing_time_reminder'], show_alert=True)

    async for session in get_async_session():
        categories = await crud_get_all_categories(
            filter=True,
            session=session
        )
        keyboard = await create_keyboard_category(
            categories=categories,
            user_id=callback.message.chat.id,
            session=session
        )
        check_working_bot = await crud_get_store_info(session=session)
        break
    if check_working_bot.is_active:
        await callback.message.edit_text(text=LEXICON_RU['category'],
                                         reply_markup=keyboard)
    else:
        await callback.answer(
            text="В настоящий момент наше заведение не работает",
            show_alert=True
        )
        await callback.message.edit_reply_markup(
            reply_markup=await create_keyboard_main(callback.message.chat.id)
        )


async def get_menu_products(
    callback: CallbackQuery,
    callback_data: CategoryIdCallbackFactory
):
    products = await get_products_by_category(
        category_id=callback_data.category_id
    )

    keyboard = await get_keyboard_products_by_category(
        products=products,
        user_id=callback.message.chat.id
    )

    if products:
        await callback.message.edit_text(text=LEXICON_RU['store'],
                                         reply_markup=keyboard)
    else:
        await callback.answer(text=LEXICON_RU['finish_category'],
                              show_alert=True)
