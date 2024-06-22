__all__ = ("router",)

from aiogram import Router

from .admin_handlers import router as admin_router
from .mailing import router as mailing_router
from .fsm_update_welcome_text import router as update_welcome_text_router
from .fsm_update_manager_group import router as update_manager_group_router
from .fsm_update_sale_group import router as update_sale_group_router
from .fsm_update_location import router as update_location_router
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
from .change_popular_product import router as change_popular_product_router
from .reports import router as reports_router
from .toggle_bot import router as toggle_router
from .change_availability_category import router as avail_category_router
from .change_availability_product import router as avail_product_router
from .fsm_add_product import router as fsm_add_prod_router
from .fsm_add_category import router as fsm_add_cat_router
from .fsm_check_order import router as fsm_check_order_router
from .fsm_create_qr import router as fsm_create_qr_router
from .fsm_custom_report import router as fsm_custom_report_router
from .fsm_resourse_report import router as fsm_resourse_report_router
from .change_delivery_base import router as change_delivery_router
from .fsm_add_district import router as fsm_add_district_router
from .fsm_mailling import router as fsm_mailling_router

router = Router(name=__name__)

router.include_routers(
    admin_router,
    fsm_check_order_router,
    fsm_create_qr_router,
    fsm_custom_report_router,
    fsm_add_prod_router,
    fsm_add_cat_router,
    fsm_resourse_report_router,
    change_popular_product_router,
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
    update_location_router,
    update_welcome_text_router,
    update_manager_group_router,
    update_sale_group_router,
    change_delivery_router,
    fsm_add_district_router,
    fsm_mailling_router,
)
