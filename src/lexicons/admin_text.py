from src.callbacks import StoreAdminCbData, StoreCbDataList


def create_report_main_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'sales_today': {
            'text': 'Продажи за день',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='sales-today'
            ).pack()
        },
        'sales_period_custom': {
            'text': 'Продажи за период',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='sales-period'
            ).pack()
        },
        'pending_orders': {
            'text': 'Заказы в очереди',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='pending-orders'
            ).pack()
        },
        'view_order': {
            'text': 'Посмотреть заказ по номеру',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='view-order'
            ).pack()
        },
        'delivery_report': {
            'text': 'Отчёт по районам доставки',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='delivery-report'
            ).pack()
        },
        'ad_report': {
            'text': 'Отчёт по рекламе',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='ad-report'
            ).pack()
        },
        'back': {
            'text': '<<< назад',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='admin'
            ).pack()
        }
    }


def create_admin_main_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'stop_list': {
            'text': 'Стоп-лист ⛔️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='stop-list'
            ).pack()
        },
        'edit_menu': {
            'text': 'Редактирование меню ✏️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='edit-menu'
            ).pack()
        },
        'edit_delivery': {
            'text': 'Редактирование районов доставки ✏️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='edit-delivery'
            ).pack()
        },
        'reports': {
            'text': 'Отчёты 📑',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='reports'
            ).pack()
        },
        'employees': {
            'text': 'Сотрудники 🧑‍🍳',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='employees'
            ).pack()
        },
        'qr_code': {
            'text': 'Сгенерировать qr-code',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='qr-code'
            ).pack()
        },
        'toggle_bot': {
            'text': 'Настройки бота ⚙️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='toggle-bot'
            ).pack()
        },
        'mailling': {
            'text': 'Рассылка',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='mailling'
            ).pack()
        },
        'main_menu': {
            'text': '<<< назад',
            'callback_data': StoreCbDataList(
                store_id=store_id,
                type_press='select-one'
            ).pack()
        }
    }


def create_edit_menu_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'modify_avail_prod': {
            'text': 'Изменить наличие (товары)',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='modify-avail-prod'
            ).pack()
        },
        'modify_avail_categ': {
            'text': 'Изменить наличие (категории)',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='modify-avail-categ'
            ).pack()
        },
        'modify_popular_prod': {
            'text': 'Изменить популярное (товары)',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='modify-popular-prod'
            ).pack()
        },
        'add_product': {
            'text': 'Добавить новый товар',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='add-product'
            ).pack()
        },
        'add_category': {
            'text': 'Добавить новую категорию',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='add-category'
            ).pack()
        },
        'change_product': {
            'text': 'Редактировать товары ✏️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='change-product'
            ).pack()
        },
        'change_category': {
            'text': 'Редактировать категории ✏️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='change-category'
            ).pack()
        },
        'back': {
            'text': '<<< назад',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='admin'
            ).pack()
        },
    }
