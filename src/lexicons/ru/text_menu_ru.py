def create_navigation_btn(bill: int) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Назад',
            'callback_data': 'press_main_menu'
        },
        'cart': {
            'text': f'Корзина 🛒 {bill} ₹',
            'callback_data': 'press_cart'
        }
    }


def create_navigation_prod_btn(bill: int) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Назад',
            'callback_data': 'press_menu'
        },
        'cart': {
            'text': f'Корзина 🛒 {bill} ₹',
            'callback_data': 'press_cart'
        }
    }


special_offer_dict: dict[str, dict[str, str]] = {
    'special_offer': {
        'text': '🔥Спецпредложение',
        'callback_data': 'press_popular_menu'
    }
}


menu_messages_dict: dict[str, str] = {
    'category': 'Выберите необходимую категорию',
    'product': 'Выберите необходимое блюдо',
    'closing_time_reminder': 'Внимание, в 23:00 мы закрываемся, но у вас ещё '
                             'есть время) не затягивайте с выбором)',
    'closing_time': 'Упс...((\n\nИзвините, оформить заказ не получится.\n'
                    'Мы работаем с 14:00 до 23:00.\n'
                    'Будем рады накормить вас в рабочие часы)',
    'finish_category': 'Извините, блюда из данной категории сейчас закончились'
                       ', они появятся в ближайшее время, а пока можете '
                       'заказать что-нибудь другое)',
    'store_not_active': 'В настоящий момент наше заведение не работает',
    'non_working_hours': 'Упс...((\n\nИзвините, оформить заказ не получится.\n'
                         'Мы работаем с 14:00 до 23:00.\n'
                         'Будем рады накормить вас в рабочие часы)',

}
