from aiogram import Router, F
from aiogram.filters import Command, CommandStart

from .start import process_start_command
from .commands import get_my_id
from .main_menu import (
    press_get_location,
    press_del_location,
    get_contact,
    get_delivery_info,
    press_main_menu,
    press_back_main_menu,
)
from .menu import get_menu_category, get_menu_products
from .cart import (
    adding_to_cart,
    press_cart,
    press_cart_edit,
    process_cart_edit,
    empty_cart,
)
from .fsm_delivery import (
    process_delivery_form_command,
    process_district_selection,
    warning_not_number,
    process_phone_sent,
    warning_not_phone,
    process_guide_sent,
    warning_not_guide,
    process_location_sent,
    warning_not_location,
    process_cancel_command_delivery,
)
from .order import (
    create_orders_takeaway,
    process_edit_status_order,
    process_time_order,
    process_edit_status_redy_order,
)
from .fsm_comment import (
    process_waiting_comment,
    process_cancel_command_state,
    process_comment_sent,
)
from .fsm_check_order import (  # noqa: F401
    process_view_order,
    process_cancel_command_state_order,
    process_waiting_order_id,
)
from .fsm_ad_report import (  # noqa: F401
    process_ad_report,
    process_cancel_command_state_resourse,
    process_waiting_resourser,
)
from .fsm_sales_period_custom import (
    process_waiting_start_date,
    process_waiting_end_date,
    process_sales_period_custom,
)
from .admin import (
    press_admin_menu,
    press_stop_list,
    process_reports,
    process_edit_hours,
    process_toggle_bot,
    process_sales_today,
    process_sales_period,
    process_pending_orders,
    process_delivery_report,
    process_modify_availability_products,
    process_modify_availability_categories,
    process_add_product,
    process_delete_product,
    process_add_category,
    process_delete_category,
    process_edit_menu,
    get_admin_products,
    get_admin_change_avail_products,
    process_press_availability_categories,
    process_toggle_working_bot,
)
from ..callbacks import (
    CategoryIdCallbackFactory,
    ProductIdCallbackFactory,
    CartEditCallbackFactory,
    CreateOrderCallbackFactory,
    DeliveryIdCallbackFactory,
    CheckOrdersCallbackFactory,
    TimeOrdersCallbackFactory,
    OrderStatusCallbackFactory,
    CategoryAdminCallbackFactory,
    ProductIdAdminCallbackFactory,
    CategoryAdminAvailCallbackFactory,
)
from ..fsm_state import (
    FSMDeliveryInfo,
    FSMComment,
    FSMCheckOrder,
    FSMSalesPeriodCustom,
    FSMAdReport,
)
from ..lexicons import LEXICON_KEYBOARDS_RU


def register_user_commands(router: Router) -> None:
    router.message.register(
        process_start_command, CommandStart()
    )
    router.message.register(process_cancel_command_delivery,
                            F.text == LEXICON_KEYBOARDS_RU['cancel_2'])

    router.message.register(process_cancel_command_state,
                            F.text == LEXICON_KEYBOARDS_RU['cancel'])

    router.message.register(get_my_id, Command('id'))

    router.callback_query.register(
        get_menu_category, F.data == 'press_menu'
    )

    router.callback_query.register(
        get_delivery_info, F.data == 'press_delivery'
    )
    router.callback_query.register(
        press_del_location, F.data == 'press_del'
    )
    router.callback_query.register(
        get_contact, F.data == 'press_contact'
    )
    router.callback_query.register(
        press_get_location, F.data == 'press_location'
    )
    # router.callback_query.register(
    #     open_personal_area, F.data == 'press_personal_area'
    # )
    router.callback_query.register(
        press_main_menu, F.data == 'press_main_menu'
    )
    router.callback_query.register(
        press_back_main_menu, F.data == 'press_back_main_menu'
    )
    router.callback_query.register(
        get_menu_products, CategoryIdCallbackFactory.filter()
    )
    router.callback_query.register(
        adding_to_cart, ProductIdCallbackFactory.filter()
    )
    router.callback_query.register(
        press_cart, F.data == 'press_cart'
    )
    router.callback_query.register(
        press_cart_edit, F.data == 'press_edit_cart'
    )
    router.callback_query.register(
        process_cart_edit, CartEditCallbackFactory.filter()
    )
    router.callback_query.register(
        empty_cart, F.data == 'press_empty'
    )
    router.callback_query.register(
        create_orders_takeaway, CreateOrderCallbackFactory.filter()
    )
    router.callback_query.register(
        create_orders_takeaway, F.data == 'press_takeaway'
    )
    router.callback_query.register(
        process_delivery_form_command,
        F.data == 'press_delivery_pay'
    )
    router.callback_query.register(
        process_district_selection,
        FSMDeliveryInfo.waiting_delivery_id,
        DeliveryIdCallbackFactory.filter()
    )
    router.message.register(
        warning_not_number,
        FSMDeliveryInfo.waiting_delivery_id
    )
    router.message.register(
        process_phone_sent,
        FSMDeliveryInfo.waiting_number_phone,
        (lambda x: x.text.isdigit() and len(x.text)
         == 10 or x.text == "Пропустить шаг")
    )
    router.message.register(
        warning_not_phone,
        FSMDeliveryInfo.waiting_number_phone
    )
    router.message.register(
        process_guide_sent,
        FSMDeliveryInfo.waiting_guide,
        F.text
    )
    router.message.register(
        warning_not_guide,
        FSMDeliveryInfo.waiting_guide
    )
    router.message.register(
        process_location_sent,
        FSMDeliveryInfo.waiting_location,
        F.location | (F.text == "Пропустить шаг")
    )
    router.message.register(
        warning_not_location,
        FSMDeliveryInfo.waiting_location
    )
    router.callback_query.register(
        process_waiting_comment, F.data == 'press_comment'
    )
    router.message.register(
        process_cancel_command_state,
        F.text == LEXICON_KEYBOARDS_RU['cancel']
    )
    router.message.register(
        process_comment_sent,
        FSMComment.waiting_comment, F.text
    )
    router.callback_query.register(
        process_edit_status_order,
        CheckOrdersCallbackFactory.filter()
    )
    router.callback_query.register(
        process_time_order,
        TimeOrdersCallbackFactory.filter()
    )
    router.callback_query.register(
        process_edit_status_redy_order,
        OrderStatusCallbackFactory.filter()
    )


def register_admin_commands(router: Router) -> None:
    router.callback_query.register(
        press_admin_menu, F.data == 'press_admin')
    router.callback_query.register(
        press_stop_list, F.data == 'press_stop_list')
    router.callback_query.register(
        process_edit_menu, F.data == 'press_edit_menu')
    router.callback_query.register(
        process_reports, F.data == 'press_reports')
    router.callback_query.register(
        process_edit_hours, F.data == 'press_edit_hours')

    router.callback_query.register(
        process_sales_today, F.data == 'press_sales_today')
    router.callback_query.register(
        process_sales_period, F.data == 'press_sales_period')
    router.callback_query.register(
        process_pending_orders, F.data == 'press_pending_orders')

    router.callback_query.register(
        process_delivery_report, F.data == 'press_delivery_report')
    router.callback_query.register(
        process_modify_availability_products,
        F.data == 'press_modify_avail_prod')

    router.callback_query.register(
        process_add_product, F.data == 'press_add_product')
    router.callback_query.register(
        process_delete_product, F.data == 'press_delete_product')
    router.callback_query.register(
        process_add_category, F.data == 'press_add_category')
    router.callback_query.register(
        process_delete_category, F.data == 'press_delete_category')
    router.callback_query.register(
        process_sales_period_custom,
        F.data == 'press_sales_period_custom'
    )
    router.message.register(
        process_waiting_start_date,
        FSMSalesPeriodCustom.start_date,
        F.text
    )
    router.message.register(
        process_waiting_end_date,
        FSMSalesPeriodCustom.end_date,
        F.text
    )
    router.callback_query.register(
        process_view_order, F.data == 'press_view_order')
    router.message.register(
        process_waiting_order_id,
        FSMCheckOrder.order_id,
        F.text
    )
    router.callback_query.register(
        process_ad_report, F.data == 'press_ad_report')
    router.message.register(
        process_waiting_resourser,
        FSMAdReport.resourse,
        F.text
    )
    router.callback_query.register(
        get_admin_products, CategoryAdminCallbackFactory.filter()
    )
    router.callback_query.register(
        get_admin_change_avail_products, ProductIdAdminCallbackFactory.filter()
    )

    router.callback_query.register(
        process_modify_availability_categories,
        F.data == 'press_modify_avail_categ')
    router.callback_query.register(
        process_press_availability_categories,
        CategoryAdminAvailCallbackFactory.filter()
    )

    router.callback_query.register(
        process_toggle_bot, F.data == 'press_toggle_bot')
    router.callback_query.register(
        process_toggle_working_bot, F.data == 'press_toggle_working_bot')
