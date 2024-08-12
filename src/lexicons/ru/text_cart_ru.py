from typing import Optional

from src.callbacks import CartCallbackData, StoreMenuCbData
from src.callbacks.order import OrderCallbackFactory
from src.utils import OrderTypes, OrderStatus


def create_btn_cart(
    store_id: int,
    mess_id: int,
    language: str
) -> dict[str, dict[str, str]]:
    btn = {
        'add_comment': {
            'text': 'Добавить комментарий',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='comment-cart'
            ).pack()
        },
        'takeaway': {
            'text': 'Самовывоз',
            'callback_data': OrderCallbackFactory(
                type_callback='create',
                order_type=OrderTypes.TAKEAWAY.value['id'],
                status=OrderStatus.NEW.value['id'],
                mess_id=mess_id,
                language=language,
                store_id=store_id
            ).pack()
        },
        'dine_in': {
            'text': 'В зале',
            'callback_data': OrderCallbackFactory(
                type_callback='create',
                order_type=OrderTypes.DINEIN.value['id'],
                status=OrderStatus.NEW.value['id'],
                mess_id=mess_id,
                language=language,
                store_id=store_id
            ).pack()
        },
        'delivery': {
            'text': 'Доставка 🚚',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='press-delivery'
            ).pack()
        },
        'main_menu': {
            'text': 'Меню',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='main-menu'
            ).pack()
        },
        'clear': {
            'text': 'Очистить',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='empty-cart'
            ).pack()
        },
        'edit': {
            'text': 'Редактировать',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='edit-cart'
            ).pack()
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


def create_edit_cart_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'main_menu': {
            'text': 'Главное меню',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='main-menu'
            ).pack()
        },
        'clear': {
            'text': 'Очистить',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='empty-cart'
            ).pack()
        },
        'checkout': {
            'text': 'Оформить',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='cart'
            ).pack()
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
            f'Дополнительная плата за упаковку*: {box_price} ₹\n'
            "--------------------\n"
            f'Итоговая сумма к оплате: {bill * 0.95 + box_price} ₹\n'
            "--------------------\n"
            f'*Плата за упаковку взымается только при доставке '
            'или самовывозе\n'
        )
    return message
