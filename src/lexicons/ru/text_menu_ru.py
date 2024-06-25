from datetime import time

from src.callbacks import StoreMenuCbData, CartCallbackData


def create_navigation_btn(
    bill: int,
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Назад',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='main-menu'
            ).pack()
        },
        'cart': {
            'text': f'Корзина 🛒 {bill} ₹',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='cart'
            ).pack()
        }
    }


def create_navigation_prod_btn(
    bill: int,
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Назад',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='menu'
            ).pack()
        },
        'cart': {
            'text': f'Корзина 🛒 {bill} ₹',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='cart'
            ).pack()
        }
    }


def create_special_offer_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'special_offer':
            {
                'text': '🔥Спецпредложение',
                'callback_data': StoreMenuCbData(
                    store_id=store_id,
                    type='popular'
                ).pack()
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


def create_non_working_hours_text(
    opening_time: time,
    closing_time: time,
) -> str:
    return (
        'Упс...((\n\nИзвините, оформить заказ не получится.\n'
        f'Мы работаем с {opening_time.strftime("%H:%M")} '
        f'до {closing_time.strftime("%H:%M")}.\n'
        'Будем рады накормить вас в рабочие часы)'
    )
