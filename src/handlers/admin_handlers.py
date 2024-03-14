import random
import os
from datetime import datetime
from aiogram import Bot, types, Router, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from src.db import customer_db
from src.lexicons import LEXICON_RU
from src.keyboards import (
    admin_kb,
    category_kb,
    main_kb,
    product_kb,
    report_kb,
    store_kb,
)
from src.config import settings
from src.db import product_db, store_db, category_db
from src.utils import report_utils
from src.callbacks import (
    CategoryAdminCallbackFactory,
    ProductIdAdminCallbackFactory,
    CategoryAdminAvailCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_admin')
async def press_admin_menu(callback: types.CallbackQuery):
    message_text = 'Выберите необходимый пункт'
    await callback.message.edit_text(
        text=message_text,
        reply_markup=admin_kb.create_kb_admin_main()
    )


async def back_admin_menu(message: types.Message):
    message_text = 'Выберите необходимый пункт'
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
        text="message_text",
        reply_markup=admin_kb.create_kb_edit_menu()
    )


@router.callback_query(F.data == 'press_reports')
async def process_reports(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )


@router.callback_query(F.data == 'press_sales_today')
async def process_sales_today(callback: types.CallbackQuery):
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        message = await report_utils.custom_summary_text(
            start_date=today,
            end_date=today
        )

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


@router.callback_query(F.data == 'press_sales_period')
async def process_sales_period(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )


async def process_sales_period_custom(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )


@router.callback_query(F.data == 'press_pending_orders')
async def process_pending_orders(callback: types.CallbackQuery):
    try:
        message = await report_utils.generate_pending_orders_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_view_order(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )


@router.callback_query(F.data == 'press_delivery_report')
async def process_delivery_report(callback: types.CallbackQuery):
    try:
        message = await report_utils.generate_delivery_report_text()

        await callback.message.edit_text(
            text=message,
            reply_markup=report_kb.create_kb_report()
        )
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


async def process_resourse_report(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=report_kb.create_kb_report()
    )


@router.callback_query(F.data == 'press_modify_avail_prod')
async def process_modify_availability_products(callback: types.CallbackQuery):
    categories = await category_db.get_all_categories()
    keyboard = await category_kb.create_kb_category_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'press_modify_avail_categ')
async def process_modify_availability_categories(
    callback: types.CallbackQuery
):
    categories = await category_db.get_all_categories_admin()
    keyboard = await category_kb.create_kb_category_avail_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=keyboard
    )


@router.callback_query(CategoryAdminAvailCallbackFactory.filter())
async def process_press_availability_categories(
    callback: types.CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    await category_db.change_avail_category(callback_data.category_id)
    categories = await category_db.get_all_categories_admin()
    keyboard = await category_kb.create_kb_category_avail_admin(
        categories=categories
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


# @router.callback_query(F.data == 'press_add_product')
# async def process_add_product(callback: types.CallbackQuery):
#     await callback.message.edit_text(
#         text="message_text",
#         reply_markup=admin_kb.create_kb_admin_main()
#     )


@router.callback_query(F.data == 'press_delete_product')
async def process_delete_product(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_kb.create_kb_admin_main()
    )


@router.callback_query(F.data == 'press_delete_category')
async def process_delete_category(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_kb.create_kb_admin_main()
    )


@router.callback_query(F.data == 'press_edit_hours')
async def process_edit_hours(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="message_text",
        reply_markup=admin_kb.create_kb_admin_main()
    )


@router.callback_query(F.data == 'press_toggle_bot')
async def process_toggle_bot(callback: types.CallbackQuery):
    store_info = await store_db.get_store_info()
    keyboard = store_kb.create_kb_toggle_bot(
        store_info=store_info
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'press_toggle_working_bot')
async def process_toggle_working_bot(callback: types.CallbackQuery):
    await store_db.change_is_active_bot()

    store_info = await store_db.get_store_info()
    keyboard = store_kb.create_kb_toggle_bot(
        store_info=store_info
    )
    await callback.message.edit_text(
        text="message_text",
        reply_markup=keyboard
    )


@router.callback_query(CategoryAdminCallbackFactory.filter())
async def get_admin_products(
    callback: types.CallbackQuery,
    callback_data: CategoryAdminCallbackFactory
):
    products = await product_db.get_products_by_category_admin(
        category_id=callback_data.category_id
    )

    keyboard = await product_kb.create_kb_product_admin(
        products=products
    )

    await callback.message.edit_text(text='Продукты',
                                     reply_markup=keyboard)
    await callback.answer(text='Ок')


@router.callback_query(ProductIdAdminCallbackFactory.filter())
async def get_admin_change_avail_products(
    callback: types.CallbackQuery,
    callback_data: ProductIdAdminCallbackFactory
):
    try:
        await product_db.change_avail_roducts(callback_data.product_id)

        products = await product_db.get_products_by_category_admin(
            category_id=callback_data.category_id
        )

        keyboard = await product_kb.create_kb_product_admin(
            products=products
        )

        await callback.message.edit_text(text='Продукты',
                                         reply_markup=keyboard)
        await callback.answer(text='Ок')
    except TelegramBadRequest:
        await callback.answer(
            text=LEXICON_RU['error'],
        )


@router.message(Command('id'))
async def get_my_id(message: types.Message):
    await message.answer(text=str(message.chat.id))


@router.message((Command('m')))
async def create_mail_group(message: types.Message, bot: Bot):
    user_info = await customer_db.get_user_info_by_id(
        user_id=message.chat.id
    )
    if user_info.admin:
        text = message.caption[2:]
        await bot.send_photo(
            chat_id=settings.SALE_GROUP,
            photo=message.photo[-1].file_id,
            caption=text,
            reply_markup=admin_kb.settings.create_kb_sale_group()
        )
        await message.answer(
            text='Пост опубликован успешно',
            reply_markup=await main_kb.create_kb_main(
                message.chat.id
            )
        )
    else:
        await message.answer(
            text='Данная команда доступна только для администраторов бота',
            reply_markup=await main_kb.create_kb_main(
                message.chat.id
            )
        )


async def create_mail_group_auto(bot: Bot):
    text = ('Всем хорошего дня 🔥\n'
            'Эта кнопка для заказа через приложение Marcello 👇\n'
            'При заказе через приложение постоянная скидка на все меню 5% 👍')

    current_dir = os.path.dirname(os.path.abspath(__file__))

    static_folder = os.path.join(current_dir, '..', 'static')

    file_list = os.listdir(static_folder)

    random_file = random.choice(file_list)

    random_file_path = os.path.join(static_folder, random_file)

    photo_file = types.FSInputFile(random_file_path)

    await bot.send_photo(
        chat_id=settings.SALE_GROUP,
        photo=photo_file,
        caption=text,
        reply_markup=admin_kb.create_kb_sale_group()
    )
