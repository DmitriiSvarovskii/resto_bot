from src.callbacks import StoreMenuCbData, CartCallbackData


def create_navigation_btn(
    bill: int,
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Back',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='main-menu'
            ).pack()},
        'cart': {
            'text': f'Cart 🛒 {bill} ₹',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='cart'
            ).pack()}
    }


def create_navigation_prod_btn(
    bill: int,
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Back',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='menu'
            ).pack()},
        'cart': {
            'text': f'Cart 🛒 {bill} ₹',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='cart'
            ).pack()}
    }


def create_special_offer_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'special_offer':
            {
                'text': '🔥Special Offer',
                'callback_data': StoreMenuCbData(
                    store_id=store_id,
                    type='popular'
                ).pack()
            }
    }


menu_messages_dict: dict[str, str] = {
    'category': 'Choose the necessary category',
    'product': 'Choose the desired dish',
    'closing_time_reminder': 'Attention, we close at 23:00, '
                             'but you still have time) '
                             'don\'t delay with your choice)',
    'closing_time': 'Oops...((\n\nSorry, we can\'t take orders now.\n'
                    'We operate from 14:00 to 23:00.\n'
                    'We\'ll be happy to serve you during our working hours)',
    'finish_category': 'Sorry, dishes from this category are currently '
                       'unavailable, '
                       'they will be available soon, but for now you can '
                       'order something else)',
    'store_not_active': 'Currently, our establishment is not operational.',
    'non_working_hours': 'Oops...((\n\n'
                         'Sorry, placing an order is not possible.\n'
                         'We operate from 14:00 to 23:00.\n'
                         "We'll be happy to serve you "
                         'during our working hours)',
}
