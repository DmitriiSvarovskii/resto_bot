from typing import List, Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from src.db import cart_db
from src.schemas import product_schemas
from src.lexicons import LEXICON_KEYBOARDS_RU
from src.callbacks import (
    ProductIdCallbackFactory,
    ProductIdAdminCallbackFactory,
    ProductChangeAdminCallbackFactory,
    ProductChangeCategoryCallbackFactory,
    ProductChangeNameCallbackFactory,
    ProductChangeDescriptionCallbackFactory,
    ProductChangePriceCallbackFactory,
    ProductChangePriceBoxCallbackFactory,
    ProductDeleteCallbackFactory,
    CategoryAdminChangeCallbackFactory,
)


async def create_kb_product(
    products: List[product_schemas.ReadProduct],
    user_id: int,
    popular: Optional[bool] = None
):
    cart_info = await cart_db.get_cart_items_and_totals(
        user_id=user_id
    )

    cart_items_dict = {
        item.product_id: item.quantity for item in cart_info.cart_items}

    keyboard = InlineKeyboardBuilder()

    for product in products:

        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductIdCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=popular
                ).pack()))

        product_quantity = cart_items_dict.get(product.id, 0)

        keyboard.row(
            InlineKeyboardButton(
                text='Состав',
                callback_data=ProductIdCallbackFactory(
                    type_pr='compound',
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=popular
                ).pack()),
            InlineKeyboardButton(
                text=f'Цена: {product.price} ₹',
                callback_data='press_pass'
            ),
            InlineKeyboardButton(
                text=f'{product_quantity} шт',
                callback_data='press_pass'),
            width=3
        )

        keyboard.row(
            InlineKeyboardButton(
                text='➖',
                callback_data=ProductIdCallbackFactory(
                    type_pr='minus',
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=popular
                ).pack()
            ),
            InlineKeyboardButton(
                text='➕',
                callback_data=ProductIdCallbackFactory(
                    type_pr='plus',
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=popular
                ).pack()
            ),
            width=2
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_menu'
        ),
        InlineKeyboardButton(
            text=f'Корзина 🛒 {cart_info.total_price} ₹',
            callback_data='press_cart'
        )
    )

    return keyboard.as_markup()


async def create_kb_product_admin(
    products: List[product_schemas.ReadProduct],
):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        availability = "В наличии" if product.availability else "Отсутствует"
        indicator = '✅' if product.availability else '❌'
        action = "Убрать" if product.availability else "Добавить"

        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()),
            InlineKeyboardButton(
                text=indicator,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=ProductIdAdminCallbackFactory(
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


async def create_kb_change_product_list(
    products: List[product_schemas.ReadProduct],
):
    keyboard = InlineKeyboardBuilder()
    for product in products:
        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductChangeAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id
                ).pack()))
    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_change_product'
        )
    )

    return keyboard.as_markup()


async def create_kb_change_product(
    product_id: int,
    category_id: int
):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text='Изменить категорию товара ✏️',
            callback_data=ProductChangeCategoryCallbackFactory(
                product_id=product_id
            ).pack()),
        InlineKeyboardButton(
            text='Изменить название товара ✏️',
            callback_data=ProductChangeNameCallbackFactory(
                product_id=product_id
            ).pack()),
        InlineKeyboardButton(
            text='Изменить описание товара ✏️',
            callback_data=ProductChangeDescriptionCallbackFactory(
                product_id=product_id
            ).pack()),
        InlineKeyboardButton(
            text='Изменить цену товара ✏️',
            callback_data=ProductChangePriceCallbackFactory(
                product_id=product_id
            ).pack()),
        InlineKeyboardButton(
            text='Изменить цену упаковки ✏️',
            callback_data=ProductChangePriceBoxCallbackFactory(
                product_id=product_id
            ).pack()),
        InlineKeyboardButton(
            text='Удалить товар ✖',
            callback_data=ProductDeleteCallbackFactory(
                product_id=product_id
            ).pack()),
        width=1
    )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data=CategoryAdminChangeCallbackFactory(
                category_id=category_id
            ).pack()),
    )

    return keyboard.as_markup()


def create_kb_fsm_change_name() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отменить изменение')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


async def create_kb_product_delete():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='press_approval_delete'
        ),
        InlineKeyboardButton(
            text='Отменить',
            callback_data='press_cancel_delete'
        ),
        width=2
    )

    return keyboard.as_markup()


async def create_kb_product_popular_admin(
    products: List[product_schemas.ReadProduct],
):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        availability = "Популяное"
        indicator = '✅' if product.popular else '❌'
        action = "Убрать" if product.popular else "Добавить"

        keyboard.row(
            InlineKeyboardButton(
                text=f'{product.name}',
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=True,
                ).pack()))

        keyboard.row(
            InlineKeyboardButton(
                text=availability,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=True,
                ).pack()),
            InlineKeyboardButton(
                text=indicator,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=True,
                ).pack()
            ),
            InlineKeyboardButton(
                text=action,
                callback_data=ProductIdAdminCallbackFactory(
                    product_id=product.id,
                    category_id=product.category_id,
                    popular=True,
                ).pack()),
            width=3
        )

    keyboard.row(
        InlineKeyboardButton(
            text=LEXICON_KEYBOARDS_RU['back'],
            callback_data='press_modify_popular_prod'
        )
    )

    return keyboard.as_markup()
