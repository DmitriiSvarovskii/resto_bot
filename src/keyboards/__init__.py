from .main_keyboard import create_keyboard_main
from .del_keyboard import create_keyboard_del
from .back_keyboard import create_keyboard_back
from .set_menu import set_main_menu
from .category import create_keyboard_category
from .product import create_keyboard_product
from .cart import create_keyboard_cart, create_keyboards_products_cart
from .order import (
    create_keyboard_back_main,
    create_keyboard_check_order,
    create_keyboard_time_cooking,
    create_order_status_keyboard,
    create_order_status_delivery_keyboard,
    create_status_redy_order_keyboard,
)
from .fsm_delivery import (
    create_keyboard_delivery,
    create_keyboard_delivery_fsm,
    create_keyboard_delivery_go,
    create_keyboard_delivery_fsm_location,
)
from .fsm_comment import create_keyboard_fsm_comment
from .admin import (
    create_keyboard_admin_main,
    create_keyboard_toggle_bot,
    create_keyboard_category_avail_admin,
    create_keyboard_edit_menu,
    create_keyboard_report,
    create_keyboard_category_admin,
    create_keyboard_product_admin,
)

from . import account_keyboards

__all__ = [
    'account_keyboards',
    'create_keyboard_main',
    'create_keyboard_delivery_fsm_location',
    'create_keyboard_del',
    'create_keyboard_back',
    'set_main_menu',
    'create_keyboard_category',
    'create_keyboard_product',
    'create_keyboard_cart',
    'create_keyboards_products_cart',
    'create_keyboard_back_main',
    'create_keyboard_check_order',
    'create_keyboard_time_cooking',
    'create_order_status_keyboard',
    'create_order_status_delivery_keyboard',
    'create_status_redy_order_keyboard',
    'create_keyboard_delivery',
    'create_keyboard_delivery_fsm',
    'create_keyboard_delivery_go',
    'create_keyboard_fsm_comment',
    'create_keyboard_admin_main',
    'create_keyboard_toggle_bot',
    'create_keyboard_category_avail_admin',
    'create_keyboard_edit_menu',
    'create_keyboard_report',
    'create_keyboard_category_admin',
    'create_keyboard_product_admin',
]
