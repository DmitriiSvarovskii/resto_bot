from src.callbacks import CreateOrderCallbackFactory
from src.services import ORDER_TYPES, ORDER_STATUSES


def my_func(mess_id: int):
    my_dict = {
        'add_comment': {
            'text': 'Добавить комментарий',
            'callback_data': 'press_comment'
        },
        'takeaway': {
            'text': 'Самовывоз',
            'callback_data': CreateOrderCallbackFactory(
                order_type=ORDER_TYPES['takeaway']['id'],
                status=ORDER_STATUSES['new']['id'],
                mess_id=mess_id,
            ).pack()
        },
        'delivery': {
            'text': 'Доставка 🚚',
            'callback_data': 'press_delivery_pay'
        },
        'main_menu': {
            'text': 'Главное меню',
            'callback_data': 'press_menu'
        },
        'clear': {
            'text': 'Очистить',
            'callback_data': 'press_empty'
        },
        'edit': {
            'text': 'Редактировать',
            'callback_data': 'press_edit_cart'
        },
    }
    return my_dict


cart_text_dict: dict[str, str] = {
    'edit_cart': 'Отредактируйте выбранные товары используя кнопки: '
                 '"➕", "➖" или "✖️".\n\n'
                 '"➕" - добавить ещё 1 единицу товара в корзину\n\n'
                 '"➖" - убрать 1 единицу товара из корзины\n\n'
                 '"✖️" - полностью удалить выбранный товар\n\n'
                 'Также вы можете полностью очистить корзину, '
                 'нажав кнопку "Очистить"\n\n',
    'empty_cart': 'Ваша корзина пуста',
    'cart_error': 'Товар в корзине отсутствует!',
}
