main_btn: dict[str, dict[str, str]] = {
    'menu': {
        'text': 'Our menu',
        'callback_data': 'press_menu'
    },
    'contact': {
        'text': 'Our contacts',
        'callback_data': 'press_contact'
    },
    'delivery': {
        'text': 'Delivery terms',
        'callback_data': 'press_delivery'
    },
    'location': {
        'text': 'Our location',
        'callback_data': 'press_location'
    },
    'personal_account': {
        'text': 'Personal account',
        'callback_data': 'press_account'
    },
    'group_telegram': {
        'text': 'Our group',
        'url': 'https://t.me/PizzaGoaFood'
    },
    'admin': {
        'text': 'Admin panel',
        'callback_data': 'press_admin'
    },
}


main_menu_dict: dict[str, str] = {
    'start': "Welcome to our pizzeria! Enjoy authentic flavors and a variety "
             "of fresh pizzas to suit every taste.",
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


def create_navigation_main_btn() -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Back',
            'callback_data': 'press_main_menu'
        },
        'cart': {
            'text': 'Main menu',
            'callback_data': 'press_main_menu'
        }
    }
