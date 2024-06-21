from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import admin_text, delivery_text


def create_kb_admin_main(
    store_id: int
):
    keyboard = InlineKeyboardBuilder()

    admin_menu_btn = admin_text.create_admin_main_btn(store_id=store_id)

    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for key, value in admin_menu_btn.items()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_edit_menu(
    store_id: int
):
    edit_menu_btn = admin_text.create_edit_menu_btn(store_id=store_id)
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for key, value in edit_menu_btn.items()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_edit_delivery(
    store_id: int
):
    keyboard = InlineKeyboardBuilder()
    delivery_btn = delivery_text.create_edit_delivery_btn(
        store_id=store_id
    )
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for key, value in delivery_btn.items()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_sale_group(
    store_id: int
):
    keyboard = InlineKeyboardBuilder()
    button_url_bot = InlineKeyboardButton(
        text='Онлайн заказ',
        url='https://t.me/Pizzeria_Marcello_bot?start=sales_group'
    )

    keyboard.row(button_url_bot, width=1)

    return keyboard.as_markup()
