from typing import List

from src.callbacks import StoreMenuCbData, StoreCbDataList, StoreAdminCbData
from src.schemas import delivery_schemas


def create_main_btn(store_id: int) -> dict[str, dict[str, str]]:
    btn = {
        'menu': {
            'text': 'Our menu',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='menu'
            ).pack()
        },
        'contact': {
            'text': 'Our contacts',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='contact'
            ).pack()
        },
        'delivery': {
            'text': 'Delivery terms',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='delivery'
            ).pack()
        },
        'location': {
            'text': 'Our location',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='location'
            ).pack()
        },
        'personal_account': {
            'text': 'Personal account',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='account'
            ).pack()
        },
        'group_telegram': {
            'text': 'Our group',
            'url': 'https://t.me/PizzaGoaFood'
        },
        'back': {
            'text': '<<< Back',
            'callback_data': StoreCbDataList(
                store_id=store_id,
                type_press='view-list'
            ).pack()
        },
        'admin': {
            'text': 'Admin panel',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='admin'
            ).pack()
        },
    }
    return btn


def create_delivery_info(
    districts: List[delivery_schemas.ReadDelivery]
) -> str:
    delivery_info = 'Delivery Information 🛵\n\nDelivery costs by area:'

    for district in districts:
        delivery_info += f'\n{district.name_rus} {district.price} ₹'

    delivery_info += (
        '\n\nP.s. Follow the prompts of our bot when placing a delivery order)'
    )

    return delivery_info


main_menu_dict: dict[str, str] = {
    'start': 'Welcome to our pizzeria 🍕🇮🇹'
    '\nEnjoy authentic tastes and '
    'a variety of Italian pizzas for everyone'
    'taste right at home 🏠'
    '\nThe delivery to your table is working 🍕🫶',
    'main_menu': "Welcome to our pizzeria! Experience true Italian flavors "
                 "from 14:00 to 23:00. Delicate dough, juicy fillings, "
                 "and a cozy atmosphere await you!\n\n",
    'store': "Our Menu",
    'delivery': 'Delivery Information 🛵'
                '\n\nDelivery costs by areas:'
                '\nMorjim 100r'
                '\nAshwem 150r'
                '\nAgarvado 150r'
                '\nSiolim 200r'
                '\nMandrem 200r'
                '\nUpper Mandrem 250r'
                '\nArambol 250r'
                '\nVagator 350r'
                '\nKerim 350r'
                '\nPaliem 350r\n\n'
                'P.S. When placing an order for delivery, '
                'follow the prompts of our bot)',
    'contact': 'Pizzeria Marcello🍕🍝\n\n'
               'The most Italian pizza in Goa🍕🍝🔥.\n\n'
               'Morjim, Turtle Beach road.\n\n'
               'For any questions, write or call\n'
               '@AyratZiganshin59\n+918149843927\n\n'
               '<a href="t.me/PizzaGoaFood">Our telegram group</a>',
    'personal_area': 'Welcome to your personal account.\n\n'
                     'You can view the history of your orders, '
                     'to see the details of the order, '
                     'click the "More" button.\n\n'
                     '"Cancel ✖️" - button to cancel the order\n\n'
                     '<i>Order cancellation is possible within '
                     '15 minutes after it is placed</i>',
    'error_private_chat': 'Sorry, this bot is intended for use only in '
                          'private chats. If you want to place an order,'
                          ' please go to the bot itself'
}

delete_location_btn = {
    'del_locations': {
        'text': 'Hide location',
        'callback_data': 'press_del'
    }
}


def create_navigation_main_btn(store_id: int) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Back',
            'callback_data': StoreCbDataList(
                store_id=store_id,
                type_press='select-one'
            ).pack()
        },
        'cart': {
            'text': 'Main menu',
            'callback_data': StoreCbDataList(
                store_id=store_id,
                type_press='select-one'
            ).pack()
        }
    }
