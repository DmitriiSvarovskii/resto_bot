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
            'text': 'Add comment',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='comment-cart'
            ).pack()
        },
        'takeaway': {
            'text': 'Takeaway',
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
            'text': 'Dine in',
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
            'text': 'Delivery 🚚',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='press-delivery'
            ).pack()
        },
        'main_menu': {
            'text': 'Menu',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='main-menu'
            ).pack()
        },
        'clear': {
            'text': 'Clear',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='empty-cart'
            ).pack()
        },
        'edit': {
            'text': 'Edit',
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
            'text': f'Total: {bill} ₹',
            'callback_data': 'press_pass'
        }
    }


edit_cart_dict: dict[str, str] = {
    'edit_cart': 'Edit your selected items using the buttons: '
                 '"➕", "➖", or "✖️".\n\n'
                 '"➕" - add 1 more unit of the item to the cart\n\n'
                 '"➖" - remove 1 unit of the item from the cart\n\n'
                 '"✖️" - completely remove the selected item\n\n'
                 'You can also clear your cart entirely by pressing the '
                 '"Clear" button\n\n',
    'empty_cart': 'Your cart is empty',
    'cart_error': 'The item is not available in the cart!',
}


def create_edit_cart_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'main_menu': {
            'text': 'Main menu',
            'callback_data': StoreMenuCbData(
                store_id=store_id,
                type='main-menu'
            ).pack()
        },
        'clear': {
            'text': 'Clear',
            'callback_data': CartCallbackData(
                store_id=store_id,
                type_press='empty-cart'
            ).pack()
        },
        'checkout': {
            'text': 'Checkout',
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
            'Your order:\n\n'
            f'{order_text}'
            "--------------------\n"
            f'Total without discount: {bill} ₹\n'
            f'Discount: {bill*0.1} ₹\n'
            f'Final price with discount: {bill*0.9} ₹\n'
        )
    else:
        message = (
            'Your order:\n\n'
            f'{order_text}'
            "\n--------------------\n"
            f'Total without discount: {bill} ₹\n'
            f'Total price with discount: {bill * 0.9} ₹\n'
            f'Order Comment: {order_comment}\n'
        )
    if box_price and box_price > 0:
        message += (
            f'Additional packaging fee*: {box_price} ₹\n'
            "--------------------\n"
            f'Total amount to be paid: {bill * 0.9 + box_price} ₹\n'
            "--------------------\n"
            "*The packaging fee is charged only upon delivery or dine-in"
        )
    return message
