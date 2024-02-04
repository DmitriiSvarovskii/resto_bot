from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from src.lexicons import LEXICON_RU
from src.keyboards import (
    create_keyboard_report,
    create_keyboard_admin_main,
    create_keyboard_edit_menu,
)
from src.callbacks import (
    CategoryAdminCallbackFactory,
    ProductIdAdminCallbackFactory,
)
from src.utils import (
    get_stop_list,
    get_store_info,
    generate_categories_avail_admin,
    generate_sales_summary_text,
    generate_pending_orders_text,
    generate_delivery_report_text,
    generate_categories_admin,
)
from .utils import (
    get_products_by_category,
    change_is_active_bot,
    change_avail_roducts,
    get_admin_keyboard_products_by_category,
    change_avail_category,
)


async def press_admin_menu(callback: CallbackQuery):
    message_text = 'Выберите необходимый пункт'
    await callback.message.edit_text(
        text=message_text,
        reply_markup=create_keyboard_admin_main()
    )


async def press_stop_list(callback: CallbackQuery, bot: Bot):
    try:
        message_text = await get_stop_list()
        if message_text is None:
            message_text = 'Стоп лист отсутствует'
        await callback.message.edit_text(
            text=message_text,
            reply_markup=create_keyboard_admin_main()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_edit_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_edit_menu()
    )


# Отчёты
async def process_reports(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_report()
    )


async def process_sales_today(callback: CallbackQuery):
    try:
        message = await generate_sales_summary_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=create_keyboard_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_sales_period(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_report()
    )


async def process_sales_period_custom(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_report()
    )


async def process_pending_orders(callback: CallbackQuery):
    try:
        message = await generate_pending_orders_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=create_keyboard_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_view_order(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_report()
    )


async def process_delivery_report(callback: CallbackQuery):
    try:
        message = await generate_delivery_report_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=create_keyboard_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_ad_report(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_report()
    )


async def process_modify_availability_products(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=await generate_categories_admin()
    )


async def process_modify_availability_categories(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=await generate_categories_avail_admin()
    )


async def process_press_availability_categories(
    callback: CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    await change_avail_category(callback_data.category_id)

    await callback.message.edit_text(
        text="message_text",
        reply_markup=await generate_categories_avail_admin()
    )


async def process_add_product(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_admin_main()
    )


async def process_delete_product(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_admin_main()
    )


async def process_add_category(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_admin_main()
    )


async def process_delete_category(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_admin_main()
    )


async def process_edit_hours(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=create_keyboard_admin_main()
    )


async def process_toggle_bot(callback: CallbackQuery):
    keyboard = await get_store_info()
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


async def process_toggle_working_bot(callback: CallbackQuery):
    await change_is_active_bot()
    keyboard = await get_store_info()
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


async def get_admin_products(
    callback: CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    products = await get_products_by_category(
        category_id=callback_data.category_id
    )

    keyboard = await get_admin_keyboard_products_by_category(
        products=products,
    )

    await callback.message.edit_text(text='Продукты',
                                     reply_markup=keyboard)
    await callback.answer(text='Ок')


async def get_admin_change_avail_products(
    callback: CallbackQuery,
    callback_data: ProductIdAdminCallbackFactory
):
    try:
        await change_avail_roducts(callback_data.product_id)

        products = await get_products_by_category(
            category_id=callback_data.category_id
        )

        keyboard = await get_admin_keyboard_products_by_category(
            products=products,
        )

        await callback.message.edit_text(text='Продукты',
                                         reply_markup=keyboard)
        await callback.answer(text='Ок')
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )
