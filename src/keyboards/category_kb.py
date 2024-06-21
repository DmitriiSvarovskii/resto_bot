from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from typing import List, Optional

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.schemas import category_schemas
from src.callbacks import (
    CategoryIdCallbackFactory,
    CategoryChangeNameCallbackFactory,
    CategoryDeleteCallbackFactory,
    CategoryAdminAvailCallbackFactory,
    CategoryAdminAddCallbackFactory,
    StoreAdminCbData
)
from src.db import cart_db
from src.lexicons import text_menu_en, text_menu_ru


async def create_kb_category(
    categories: List[category_schemas.GetCategory],
    user_id: int,
    store_id: int,
    language: str
):
    bill = await cart_db.get_total_price_cart(
        user_id=user_id,
        store_id=store_id
    )

    keyboard = InlineKeyboardBuilder()
    if language == 'ru':
        text_menu = text_menu_ru
    else:
        text_menu = text_menu_en

    text_menu_btn = text_menu.create_navigation_btn(
        bill=bill,
        store_id=store_id
    )

    text_popular_btn = text_menu.create_special_offer_btn(
        store_id=store_id
    )

    row_buttons = [InlineKeyboardButton(
        text=value['text'],
        callback_data=value['callback_data']
    ) for value in text_popular_btn.values()]

    for category in categories:
        category_name = (category.name_rus
                         if language == 'ru'
                         else category.name_en)
        row_buttons.append(
            InlineKeyboardButton(
                text=f'{category_name}',
                callback_data=CategoryIdCallbackFactory(
                    category_id=category.id,
                    store_id=store_id).pack()
            )
        )

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    for value in text_menu_btn.values():
        row_buttons.append(InlineKeyboardButton(
            text=value['text'],
            callback_data=value['callback_data']
        ))

    keyboard.row(*row_buttons, width=2)

    return keyboard.as_markup()


async def create_kb_category_admin(
    categories: List[category_schemas.GetCategory],
    callback_data: CallbackData,
    language: str,
    store_id: int,
    popular: Optional[bool] = None
):

    keyboard = InlineKeyboardBuilder()

    row_buttons = [
        InlineKeyboardButton(
            text=f'{category_name}',
            callback_data=callback_data(
                category_id=category.id,
                popular=popular,
                store_id=store_id).pack()
        )
        for category in categories
        for category_name in [category.name_rus
                              if language == 'ru'
                              else category.name_en]
    ]

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    keyboard.row(*row_buttons, width=2)

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data=StoreAdminCbData(
                store_id=store_id, type_press='edit-menu').pack()
        )
    )

    return keyboard.as_markup()


async def create_kb_category_admin_add_prod(
    categories: List[category_schemas.GetCategory],
    language: str,
    store_id: int,
):

    keyboard = InlineKeyboardBuilder()

    row_buttons = [
        InlineKeyboardButton(
            text=category_name,
            callback_data=CategoryAdminAddCallbackFactory(
                category_id=category.id,
                store_id=store_id
            ).pack()
        )
        for category in categories
        for category_name in [category.name_rus
                              if language == 'ru'
                              else category.name_en]
    ]

    if len(row_buttons) % 2 == 1:
        row_buttons.append(InlineKeyboardButton(
            text=' ', callback_data='press_pass'))

    keyboard.row(*row_buttons, width=2)

    return keyboard.as_markup()


async def create_kb_category_avail_admin(
    categories: List[category_schemas.GetCategory],
    language: str,
    store_id: int
):

    keyboard = InlineKeyboardBuilder()

    for category in categories:
        availability = "В наличии" if category.availability else "Отсутствует"
        indicator = '✅' if category.availability else '❌'
        action = "Убрать" if category.availability else "Добавить"
        category_name = (
            category.name_rus if language == 'ru' else category.name_en
        )
        keyboard.row(
            InlineKeyboardButton(
                text=category_name,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id, store_id=store_id).pack()
            ))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id, store_id=store_id).pack()
            ),
            InlineKeyboardButton(
                text=indicator,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id, store_id=store_id).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=CategoryAdminAvailCallbackFactory(
                    category_id=category.id, store_id=store_id).pack()
            ),
            width=3
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data=StoreAdminCbData(
                store_id=store_id, type_press='edit-menu').pack()
        )
    )

    return keyboard.as_markup()


async def create_kb_change_category(
    category_id: int,
    store_id: int
):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text='Изменить название категории ✏️',
            callback_data=CategoryChangeNameCallbackFactory(
                category_id=category_id, store_id=store_id
            ).pack()),
        InlineKeyboardButton(
            text='Удалить товар ✖',
            callback_data=CategoryDeleteCallbackFactory(
                category_id=category_id, store_id=store_id
            ).pack()),
        width=1
    )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data=StoreAdminCbData(
                store_id=store_id, type_press='edit-menu').pack()
        )
    )

    return keyboard.as_markup()


def create_kb_fsm_change_name() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отменить изменение')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


async def create_kb_category_delete():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='press_approval_delete_category'
        ),
        InlineKeyboardButton(
            text='Отменить',
            callback_data='press_cancel_delete_category'
        ),
        width=2
    )

    return keyboard.as_markup()
