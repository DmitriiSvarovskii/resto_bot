__all__ = ("router",)

from aiogram import Router

from .admin_handlers import router as admin_router
from .mailing import router as mailing_router
from .fsm_edit_opening_hours import router as edit_opening_hours_router
from .fsm_product_change_name import router as product_change_name_router
from .fsm_product_change_category import router as prod_change_categ_router
from .fsm_product_change_description import router as prod_change_descr_router
from .fsm_product_change_price import router as product_change_price_router
from .fsm_product_change_price_box import router as prod_chan_price_box_router
from .fsm_product_delete import router as product_delete_router
from .change_product_base import router as change_product_router
from .fsm_category_delete import router as category_delete_router
from .fsm_category_change_name import router as category_change_name_router
from .change_category_base import router as change_category_router
from .reports import router as reports_router
from .toggle_bot import router as toggle_router
from .change_availability_category import router as avail_category_router
from .change_availability_product import router as avail_product_router
from .fsm_add_product import router as fsm_add_prod_router
from .fsm_add_category import router as fsm_add_cat_router
from .cart_handlers import router as cart_router
from .fsm_check_order import router as fsm_check_order_router
from .fsm_comment import router as fsm_comment_router
from .fsm_create_qr import router as fsm_create_qr_router
from .fsm_custom_report import router as fsm_custom_report_router
from .fsm_delivery import router as fsm_delivery_router
from .fsm_resourse_report import router as fsm_resourse_report_router
from .main_menu_handlers import router as main_menu_router
from .menu_handlers import router as menu_router
from .order_handlers import router as order_router
from .start_handlers import router as start_router
from .common_handlers import router as common_router

router = Router(name=__name__)

router.include_routers(
    common_router,
    start_router,
    main_menu_router,
    menu_router,
    cart_router,
    fsm_comment_router,
    fsm_delivery_router,
    order_router,
    admin_router,
    fsm_check_order_router,
    fsm_create_qr_router,
    fsm_custom_report_router,
    fsm_add_prod_router,
    fsm_add_cat_router,
    fsm_resourse_report_router,
    avail_category_router,
    avail_product_router,
    reports_router,
    toggle_router,
    mailing_router,
    change_product_router,
    product_change_name_router,
    prod_change_categ_router,
    prod_change_descr_router,
    product_change_price_router,
    prod_chan_price_box_router,
    product_delete_router,
    category_delete_router,
    category_change_name_router,
    change_category_router,
    edit_opening_hours_router,
)
