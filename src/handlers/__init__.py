__all__ = ("router",)

from aiogram import Router

from .admin_handlers import router as admin_router
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
    fsm_resourse_report_router,
)

# router.include_router(common_router)

# from aiogram import Router, F
# from aiogram.filters import Command, CommandStart


# from .start_handlers import process_start_command
# from .admin_handlers import get_my_id, create_mail_group,
# create_mail_group_auto
# from .main_menu_handlers import (
#     press_get_location,
#     press_del_location,
#     get_contact,
#     get_delivery_info,
#     press_main_menu,
#     press_back_main_menu,
# )
# from .menu_handlers import get_menu_category, get_menu_products
# from .cart_handlers import (
#     adding_to_cart,
#     press_cart,
#     press_cart_edit,
#     process_cart_edit,
#     empty_cart,
# )
# from .fsm_delivery import (
#     process_delivery_form_command,
#     process_district_selection,
#     warning_not_number,
#     process_phone_sent,
#     warning_not_phone,
#     process_guide_sent,
#     warning_not_guide,
#     process_location_sent,
#     warning_not_location,
#     process_cancel_command_delivery,
# )
# from .order_handlers import (
#     create_orders_takeaway,
#     process_edit_status_order,
#     process_time_order,
#     process_edit_status_redy_order,
#     process_open_account,
# )
# from .fsm_comment import (
#     process_waiting_comment,
#     process_cancel_command_state,
#     process_comment_sent,
# )
# from .fsm_create_qr import (
#     process_waiting_link,
#     process_cancel_create_qr_state,
#     process_create_qr_code,
# )
# from .fsm_check_order import (  # noqa: F401
#     process_view_order,
#     process_cancel_command_state_order,
#     process_waiting_order_id,
# )
# from .fsm_resourse_report import (  # noqa: F401
#     process_resourse_report,
#     process_cancel_command_state_resourse,
#     process_waiting_resourser,
# )
# from .fsm_custom_report import (
#     process_waiting_start_date,
#     process_waiting_end_date,
#     process_sales_period_custom,
# )
# from .admin_handlers import (
#     press_admin_menu,
#     press_stop_list,
#     process_reports,
#     process_edit_hours,
#     process_toggle_bot,
#     process_sales_today,
#     process_sales_period,
#     process_pending_orders,
#     process_delivery_report,
#     process_modify_availability_products,
#     process_modify_availability_categories,
#     process_add_product,
#     process_delete_product,
#     process_add_category,
#     process_delete_category,
#     process_edit_menu,
#     get_admin_products,
#     get_admin_change_avail_products,
#     process_press_availability_categories,
#     process_toggle_working_bot,
# )
# from src.callbacks import (
#     CategoryIdCallbackFactory,
#     ProductIdCallbackFactory,
#     CartEditCallbackFactory,
#     CreateOrderCallbackFactory,
#     DeliveryIdCallbackFactory,
#     CheckOrdersCallbackFactory,
#     TimeOrdersCallbackFactory,
#     OrderStatusCallbackFactory,
#     CategoryAdminCallbackFactory,
#     ProductIdAdminCallbackFactory,
#     CategoryAdminAvailCallbackFactory,
# )
# from src.state import (
#     FSMDeliveryInfo,
#     FSMComment,
#     FSMCheckOrder,
#     FSMSalesPeriodCustom,
#     FSMAdReport,
#     FSMQrCode,
# )
# from src.lexicons import LEXICON_KEYBOARDS_RU


# def register_user_commands(router: Router) -> None:
# router.message.register(
#     process_start_command, CommandStart()
# )
# router.message.register(process_cancel_command_delivery,
#                         F.text == LEXICON_KEYBOARDS_RU['cancel_2'])

# router.message.register(process_cancel_command_state,
#                         F.text == LEXICON_KEYBOARDS_RU['cancel'])

# router.message.register(get_my_id, Command('id'))

# router.callback_query.register(
#     get_menu_category, F.data == 'press_menu'
# )

# router.callback_query.register(
#     get_delivery_info, F.data == 'press_delivery'
# )
# router.callback_query.register(
#     press_del_location, F.data == 'press_del'
# )
# router.callback_query.register(
#     get_contact, F.data == 'press_contact'
# )
# router.callback_query.register(
#     press_get_location, F.data == 'press_location'
# )
# router.callback_query.register(
#     process_open_account, F.data == 'press_account'
# )
# router.callback_query.register(
#     press_main_menu, F.data == 'press_main_menu'
# )
# router.callback_query.register(
#     press_back_main_menu, F.data == 'press_back_main_menu'
# )
# router.callback_query.register(
#     get_menu_products, CategoryIdCallbackFactory.filter()
# )
# router.callback_query.register(
#     adding_to_cart, ProductIdCallbackFactory.filter()
# )
# router.callback_query.register(
#     press_cart, F.data == 'press_cart'
# )
# router.callback_query.register(
#     press_cart_edit, F.data == 'press_edit_cart'
# )
# router.callback_query.register(
#     process_cart_edit, CartEditCallbackFactory.filter()
# )
# router.callback_query.register(
#     empty_cart, F.data == 'press_empty'
# )
# router.callback_query.register(
#     create_orders_takeaway, CreateOrderCallbackFactory.filter()
# )
# router.callback_query.register(
#     create_orders_takeaway, F.data == 'press_takeaway'
# )
# router.callback_query.register(
#     process_delivery_form_command,
#     F.data == 'press_delivery_pay'
# )
# # router.callback_query.register(
#     process_district_selection,
#     FSMDeliveryInfo.waiting_delivery_id,
#     DeliveryIdCallbackFactory.filter()
# )
# router.message.register(
#     warning_not_number,
#     FSMDeliveryInfo.waiting_delivery_id
# )
# router.message.register(
#     process_phone_sent,
#     FSMDeliveryInfo.waiting_number_phone,
#     (lambda x: x.text.isdigit() and len(x.text)
#      == 10 or x.text == "Пропустить шаг")
# )
# router.message.register(
#     warning_not_phone,
#     FSMDeliveryInfo.waiting_number_phone
# )
# router.message.register(
#     process_guide_sent,
#     FSMDeliveryInfo.waiting_guide,
#     F.text
# )
# router.message.register(
#     warning_not_guide,
#     FSMDeliveryInfo.waiting_guide
# )
# router.message.register(
#     process_location_sent,
#     FSMDeliveryInfo.waiting_location,
#     F.location | (F.text == "Пропустить шаг")
# )
# router.message.register(
#     warning_not_location,
#     FSMDeliveryInfo.waiting_location
# )
# router.callback_query.register(
#     process_waiting_comment, F.data == 'press_comment'
# )
# router.message.register(
#     process_cancel_command_state,
#     F.text == LEXICON_KEYBOARDS_RU['cancel']
# )
# router.message.register(
#     process_comment_sent,
#     FSMComment.waiting_comment, F.text
# )
# router.callback_query.register(
#     process_edit_status_order,
#     CheckOrdersCallbackFactory.filter()
# )
# router.callback_query.register(
#     process_time_order,
#     TimeOrdersCallbackFactory.filter()
# )
# router.callback_query.register(
#     process_edit_status_redy_order,
#     OrderStatusCallbackFactory.filter()
# )


# def register_admin_commands(router: Router) -> None:
# router.callback_query.register(
#     press_admin_menu, F.data == 'press_admin')
# router.callback_query.register(
#     press_stop_list, F.data == 'press_stop_list')
# router.callback_query.register(
#     process_edit_menu, F.data == 'press_edit_menu')
# router.callback_query.register(
#     process_reports, F.data == 'press_reports')
# router.callback_query.register(
#     process_edit_hours, F.data == 'press_edit_hours')

# router.callback_query.register(
#     process_sales_today, F.data == 'press_sales_today')
# router.callback_query.register(
#     process_sales_period, F.data == 'press_sales_period')
# router.callback_query.register(
#     process_pending_orders, F.data == 'press_pending_orders')

# router.callback_query.register(
#     process_delivery_report, F.data == 'press_delivery_report')
# router.callback_query.register(
#     process_modify_availability_products,
#     F.data == 'press_modify_avail_prod')

# router.callback_query.register(
#     process_add_product, F.data == 'press_add_product')
# router.callback_query.register(
#     process_delete_product, F.data == 'press_delete_product')
# router.callback_query.register(
#     process_add_category, F.data == 'press_add_category')
# router.callback_query.register(
#     process_delete_category, F.data == 'press_delete_category')
# router.callback_query.register(
#     process_sales_period_custom,
#     F.data == 'press_sales_period_custom'
# )
# router.message.register(
#     process_waiting_start_date,
#     FSMSalesPeriodCustom.start_date,
#     F.text
# )
# router.message.register(
#     process_waiting_end_date,
#     FSMSalesPeriodCustom.end_date,
#     F.text
# )
# router.callback_query.register(
#     process_view_order, F.data == 'press_view_order')
# router.message.register(
#     process_waiting_order_id,
#     FSMCheckOrder.order_id,
#     F.text
# )
# router.callback_query.register(
#     process_resourse_report, F.data == 'press_ad_report')
# router.message.register(
#     process_waiting_resourser,
#     FSMAdReport.resourse,
#     F.text
# )
# router.callback_query.register(
#     get_admin_products, CategoryAdminCallbackFactory.filter()
# )
# router.callback_query.register(
#     get_admin_change_avail_products, ProductIdAdminCallbackFactory.filter()
# )

# router.callback_query.register(
#     process_modify_availability_categories,
#     F.data == 'press_modify_avail_categ')
# router.callback_query.register(
#     process_press_availability_categories,
#     CategoryAdminAvailCallbackFactory.filter()
# )

# router.callback_query.register(
#     process_toggle_bot, F.data == 'press_toggle_bot')
# router.callback_query.register(
#     process_toggle_working_bot, F.data == 'press_toggle_working_bot')
# router.message.register(create_mail_group, (Command('m')))

# router.callback_query.register(
#     process_waiting_link, F.data == 'press_qr_code'
# )
# router.message.register(
#     process_cancel_create_qr_state,
#     F.text == LEXICON_KEYBOARDS_RU['cancel_qr']
# )
# router.message.register(
#     process_create_qr_code,
#     FSMQrCode.waiting_link, F.text
# )
