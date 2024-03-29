from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons import admin_text, delivery_text


def create_kb_admin_main():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in admin_text.admin_main_dict.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_edit_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in admin_text.edit_menu_dict.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_edit_delivery():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=value['text'], callback_data=value['callback_data'])
        for value in delivery_text.edit_delivery_dict.values()
    ]

    keyboard.row(*buttons, width=1)

    return keyboard.as_markup()


def create_kb_sale_group():
    keyboard = InlineKeyboardBuilder()
    button_url_bot = InlineKeyboardButton(
        text='Онлайн заказ',
        url='https://t.me/Pizzeria_Marcello_bot?start=sales_group'
    )

    keyboard.row(button_url_bot, width=1)

    return keyboard.as_markup()
