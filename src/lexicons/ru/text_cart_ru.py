from typing import Optional

from src.callbacks import CreateOrderCallbackFactory
from src.callbacks.order import OrderCallbackFactory
from src.utils import OrderTypes, OrderStatus


def create_btn_cart(mess_id: int, language: str) -> dict[str, dict[str, str]]:
    btn = {
        'add_comment': {
            'text': 'Добавить комментарий',
            'callback_data': 'press_comment'
        },
        'takeaway': {
            'text': 'Самовывоз',
            'callback_data': OrderCallbackFactory(
                type_callback='create',
                order_type=OrderTypes.TAKEAWAY.value['id'],
                status=OrderStatus.NEW.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        },
        'dine_in': {
            'text': 'В зале',
            'callback_data': OrderCallbackFactory(
                type_callback='create',
                order_type=OrderTypes.DINEIN.value['id'],
                status=OrderStatus.NEW.value['id'],
                mess_id=mess_id,
                language=language
            ).pack()
        },
        'delivery': {
            'text': 'Доставка 🚚',
            'callback_data': 'press_delivery_pay'
        },
        'main_menu': {
            'text': 'Меню',
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
    return btn


def create_total_btn(bill: int) -> dict[str, dict[str, str]]:
    return {
        'total': {
            'text': f'Итого: {bill} ₹',
            'callback_data': 'press_pass'
        }
    }


edit_cart_dict: dict[str, str] = {
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


edit_btn_cart_dict: dict[str, dict[str, str]] = {
    'main_menu': {
        'text': 'Главное меню',
        'callback_data': 'press_main_menu'
    },
    'clear': {
        'text': 'Очистить',
        'callback_data': 'press_empty'
    },
    'checkout': {
        'text': 'Оформить',
        'callback_data': 'press_cart'
    }
}


def create_cart_text(
        bill: int,
        order_text: str,
        order_comment: Optional[str] = None,
        box_price: Optional[int] = None
):
    if not order_comment:
        message = (
            'Ваш заказ:\n\n'
            f'{order_text}'
            "--------------------\n"
            f'Итого без скидки: {bill} ₹\n'
            f'Скидка: {bill*0.05} ₹\n'
            f'Итоговая цена со скидкой: {bill*0.95} ₹\n'
        )
    else:
        message = (
            'Ваш заказ:\n\n'
            f'{order_text}'
            "--------------------\n"
            f'Итого без скидки: {bill} ₹\n'
            f'Итого цена со скидкой: {bill * 0.95} ₹\n'
            f'Комментарий к заказу: {order_comment}\n'
        )
    if box_price and box_price > 0:
        message += (
            f'Дополнительная плата за упаковку: {box_price} ₹\n'
            "--------------------\n"
            f'Итоговая сумма к оплате:: {bill * 0.95 + box_price} ₹\n'
        )
    return message
