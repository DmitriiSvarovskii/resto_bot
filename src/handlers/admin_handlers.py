from src.db import customer_db
from aiogram.types import Message
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from datetime import datetime

from src.lexicons import LEXICON_RU
from src.keyboards import (
    report_keyboards,
    admin_keyboards,
    store_keyboards,
    category_keyboards,
    product_keyboards,
    main_keyboards,
)
from src.config import SALE_GROUP
from src.db import product_db, store_db, category_db
from src.utils import report_utils

from src.callbacks import (
    CategoryAdminCallbackFactory,
    ProductIdAdminCallbackFactory,
)


async def press_admin_menu(callback: CallbackQuery):
    message_text = 'Выберите необходимый пункт'
    await callback.message.edit_text(
        text=message_text,
        reply_markup=admin_keyboards.create_keyboard_admin_main()
    )


async def press_stop_list(callback: CallbackQuery, bot: Bot):
    try:
        message_text = await report_utils.create_text_stop_list()
        if message_text is None:
            message_text = 'Стоп лист отсутствует'
        await callback.message.edit_text(
            text=message_text,
            reply_markup=admin_keyboards.create_keyboard_admin_main()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_edit_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_keyboards.create_keyboard_edit_menu()
    )


# Отчёты
async def process_reports(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_sales_today(callback: CallbackQuery):
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        message = await report_utils.custom_summary_text(
            start_date=today,
            end_date=today
        )

        await callback.message.edit_text(
            text=message,
            reply_markup=report_keyboards.create_keyboard_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_sales_period(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_sales_period_custom(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_pending_orders(callback: CallbackQuery):
    try:
        message = await report_utils.generate_pending_orders_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=report_keyboards.create_keyboard_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_view_order(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_delivery_report(callback: CallbackQuery):
    try:
        message = await report_utils.generate_delivery_report_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=report_keyboards.create_keyboard_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_resourse_report(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_keyboards.create_keyboard_report()
    )


async def process_modify_availability_products(callback: CallbackQuery):
    categories = category_db.get_all_categories()
    keyboard = await category_keyboards.create_keyboard_category_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


async def process_modify_availability_categories(callback: CallbackQuery):
    categories = category_db.get_all_categories()
    keyboard = await category_keyboards.create_keyboard_category_avail_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


async def process_press_availability_categories(
    callback: CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    await category_db.change_avail_category(callback_data.category_id)
    categories = category_db.get_all_categories()
    keyboard = await category_keyboards.create_keyboard_category_avail_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


async def process_add_product(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_keyboards.create_keyboard_admin_main()
    )


async def process_delete_product(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_keyboards.create_keyboard_admin_main()
    )


async def process_add_category(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_keyboards.create_keyboard_admin_main()
    )


async def process_delete_category(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_keyboards.create_keyboard_admin_main()
    )


async def process_edit_hours(callback: CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_keyboards.create_keyboard_admin_main()
    )


async def process_toggle_bot(callback: CallbackQuery):
    store_info = await store_db.get_store_info()
    keyboard = store_keyboards.create_keyboard_toggle_bot(
        store_info=store_info
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


async def process_toggle_working_bot(callback: CallbackQuery):
    await store_db.change_is_active_bot()

    store_info = await store_db.get_store_info()
    keyboard = store_keyboards.create_keyboard_toggle_bot(
        store_info=store_info
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


async def get_admin_products(
    callback: CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    products = await product_db.get_products_by_category_admin(
        category_id=callback_data.category_id
    )

    keyboard = await product_keyboards.create_keyboard_product_admin(
        products=products
    )

    await callback.message.edit_text(text='Продукты',
                                     reply_markup=keyboard)
    await callback.answer(text='Ок')


async def get_admin_change_avail_products(
    callback: CallbackQuery,
    callback_data: ProductIdAdminCallbackFactory
):
    try:
        await product_db.change_avail_roducts(callback_data.product_id)

        products = await product_db.get_products_by_category_admin(
            category_id=callback_data.category_id
        )

        keyboard = await product_keyboards.create_keyboard_product_admin(
            products=products
        )

        await callback.message.edit_text(text='Продукты',
                                         reply_markup=keyboard)
        await callback.answer(text='Ок')
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def get_my_id(message: Message):
    await message.answer(text=str(message.chat.id))


async def create_mail_group(message: Message, bot: Bot):
    status_admin = await customer_db.get_admin_status_by_user_id(
        user_id=message.chat.id
    )
    if status_admin:
        text = message.caption[2:]
        await bot.send_photo(
            chat_id=SALE_GROUP,
            photo=message.photo[-1].file_id,
            caption=text,
            reply_markup=admin_keyboards.create_keyboard_sale_group()
        )
        await message.answer(
            text='Пост опубликован успешно',
            reply_markup=await main_keyboards.create_keyboard_main(
                message.chat.id
            )
        )
    else:
        await message.answer(
            text='Данная команда доступна только для администраторов бота',
            reply_markup=await main_keyboards.create_keyboard_main(
                message.chat.id
            )
        )
