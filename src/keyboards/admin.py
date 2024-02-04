from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional, List


from src.lexicons import LEXICON_KEYBOARDS_RU
from src.schemas import ReadProduct, GetCategory, GetStore
from src.callbacks import (
    CategoryAdminCallbackFactory,
    ProductIdAdminCallbackFactory,
    CategoryAdminAvailCallbackFactory,
)


def create_keyboard_admin_main():
    buttons = [
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['stop_list'],
            callback_data='press_stop_list'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['edit_menu'],
            callback_data='press_edit_menu'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['reports'],
            callback_data='press_reports'),
        InlineKeyboardButton(
            text="Сотрудники",
            callback_data='press_employees'),
        InlineKeyboardButton(
            text='Редактировать режим работы',
            callback_data='press_edit_hours'),
        InlineKeyboardButton(
            text='Вкл/выкл бота',
            callback_data='press_toggle_bot'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_main_menu'),
    ]

    keyboard = InlineKeyboardBuilder()

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_keyboard_report():
    buttons = [
        InlineKeyboardButton(
            text='Продажи за день',
            callback_data='press_sales_today'),
        InlineKeyboardButton(
            text='Продажи за период',
            callback_data='press_sales_period_custom'),
        InlineKeyboardButton(
            text='Заказы в очереди',
            callback_data='press_pending_orders'),
        InlineKeyboardButton(
            text='Посмотреть заказ по номеру',
            callback_data='press_view_order'),
        InlineKeyboardButton(
            text='Отчёт по районам доставки',
            callback_data='press_delivery_report'),
        InlineKeyboardButton(
            text='Отчёт по рекламе',
            callback_data='press_ad_report'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_admin'),
    ]

    keyboard = InlineKeyboardBuilder()

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_keyboard_edit_menu():
    buttons = [
        InlineKeyboardButton(
            text='Изменить наличие (товары)',
            callback_data='press_modify_avail_prod'),
        InlineKeyboardButton(
            text='Изменить наличие (категории)',
            callback_data='press_modify_avail_categ'),
        InlineKeyboardButton(
            text='Добавить новый товар',
            callback_data='press_add_product'),
        InlineKeyboardButton(
            text='Удалить товар',
            callback_data='press_delete_product'),
        InlineKeyboardButton(
            text='Добавить новую категорию',
            callback_data='press_add_category'),
        InlineKeyboardButton(
            text='Удалить категорию',
            callback_data='press_delete_category'),
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_admin'),
    ]

    keyboard = InlineKeyboardBuilder()

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


async def create_keyboard_product_admin(
    products: List[ReadProduct],
    # session: AsyncSession,
):

    keyboard = InlineKeyboardBuilder()

    for product in products:
        if product.availability:
            availability = "В наличии"
            indicator = '✅'
            action = "Убрать"
        else:
            availability = "Отсутствует"
            indicator = '❌'
            action = "Добавить"

        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductIdAdminCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=ProductIdAdminCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()),
            InlineKeyboardButton(
                text=indicator,
                callback_data=ProductIdAdminCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=ProductIdAdminCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()),
            width=3
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_modify_avail_prod'
        )
    )

    return keyboard.as_markup()


async def create_keyboard_category_admin(
    categories: List[GetCategory],
):

    keyboard = InlineKeyboardBuilder()

    row_buttons = []

    for category in categories:

        button = InlineKeyboardButton(
            text=f'{category.name}',
            callback_data=CategoryAdminCallbackFactory(
                category_id=category.id).pack()
        )
        row_buttons.append(button)

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    keyboard.row(*row_buttons, width=2)

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_edit_menu'
        )
    )

    return keyboard.as_markup()


async def create_keyboard_category_avail_admin(
    categories: List[GetCategory],
):

    keyboard = InlineKeyboardBuilder()

    for category in categories:
        if category.availability:
            availability = "В наличии"
            indicator = '✅'
            action = "Убрать"
        else:
            availability = "Отсутствует"
            indicator = '❌'
            action = "Добавить"

        keyboard.row(
            InlineKeyboardButton(
                text=f'{category.name}',
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ),
            InlineKeyboardButton(
                text=indicator,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id).pack()
            ),
            width=3
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_edit_menu'
        )
    )

    return keyboard.as_markup()


def create_keyboard_toggle_bot(store_info: Optional[GetStore]):
    keyboard = InlineKeyboardBuilder()

    if store_info.is_active:
        is_active = "Работает"
        indicator = '✅'
        action = "Выключить"
    else:
        is_active = "Выключён"
        indicator = '❌'
        action = "Включить"

    keyboard.row(
        InlineKeyboardButton(
            text=f'{store_info.name}',
            callback_data='press_toggle_working_bot')
    )

    keyboard.row(
        InlineKeyboardButton(
            text=is_active,
            callback_data='press_toggle_working_bot'),
        InlineKeyboardButton(
            text=indicator,
            callback_data='press_toggle_working_bot'),
        InlineKeyboardButton(
            text=action,
            callback_data='press_toggle_working_bot'),
        width=3
    )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_admin'
        )
    )

    return keyboard.as_markup()
