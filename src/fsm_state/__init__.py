from .fsm_delivery import FSMDeliveryInfo
from .fsm_comment import FSMComment
from .fsm_sales_period_custom import FSMSalesPeriodCustom
from .fsm_check_order import FSMCheckOrder
from .frm_ad_report import FSMAdReport


__all__ = [
    'FSMDeliveryInfo',
    'FSMComment',
    'FSMCheckOrder',
    'FSMAdReport',
    'FSMSalesPeriodCustom',
    'user_dict_comment',
    'user_dict',
    'admin_check_order',
]

user_dict_comment: dict[int, dict[str, str | int | bool]] = {}

user_dict: dict[int, dict[str, str | int | bool]] = {}

admin_check_order: dict[int, dict[str, str | int | bool]] = {}
