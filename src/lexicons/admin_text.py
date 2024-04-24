report_main_dict = {
    'sales_today': {
        'text': 'Продажи за день',
        'callback_data': 'press_sales_today'
    },
    'sales_period_custom': {
        'text': 'Продажи за период',
        'callback_data': 'press_sales_period_custom'
    },
    'pending_orders': {
        'text': 'Заказы в очереди',
        'callback_data': 'press_pending_orders'
    },
    'view_order': {
        'text': 'Посмотреть заказ по номеру',
        'callback_data': 'press_view_order'
    },
    'delivery_report': {
        'text': 'Отчёт по районам доставки',
        'callback_data': 'press_delivery_report'
    },
    'ad_report': {
        'text': 'Отчёт по рекламе',
        'callback_data': 'press_ad_report'
    },
    'back': {
        'text': '<<< назад',
        'callback_data': 'press_admin'
    }
}


admin_main_dict = {
    'stop_list': {
        'text': 'Стоп-лист ⛔️',
        'callback_data': 'press_stop_list'
    },
    'edit_menu': {
        'text': 'Редактирование меню ✏️',
        'callback_data': 'press_edit_menu'
    },
    'edit_delivery': {
        'text': 'Редактирование районов доставки ✏️',
        'callback_data': 'press_edit_delivery'
    },
    'reports': {
        'text': 'Отчёты 📑',
        'callback_data': 'press_reports'
    },
    'employees': {
        'text': 'Сотрудники 🧑‍🍳',
        'callback_data': 'press_employees'
    },
    'qr_code': {
        'text': 'Сгенерировать qr-code',
        'callback_data': 'press_qr_code'
    },
    'toggle_bot': {
        'text': 'Настройки бота ⚙️',
        'callback_data': 'press_toggle_bot'
    },
    'mailling': {
        'text': 'Рассылка',
        'callback_data': 'press_mailling'
    },
    'main_menu': {
        'text': '<<< назад',
        'callback_data': 'press_main_menu'
    }
}

edit_menu_dict = {
    'modify_avail_prod': {
        'text': 'Изменить наличие (товары)',
        'callback_data': 'press_modify_avail_prod'
    },
    'modify_avail_categ': {
        'text': 'Изменить наличие (категории)',
        'callback_data': 'press_modify_avail_categ'
    },
    'modify_popular_prod': {
        'text': 'Изменить популярное (товары)',
        'callback_data': 'press_modify_popular_prod'
    },
    'add_product': {
        'text': 'Добавить новый товар',
        'callback_data': 'press_add_product'
    },
    'add_category': {
        'text': 'Добавить новую категорию',
        'callback_data': 'press_add_category'
    },
    'change_product': {
        'text': 'Редактировать товары ✏️',
        'callback_data': 'press_change_product'
    },
    'change_category': {
        'text': 'Редактировать категории ✏️',
        'callback_data': 'press_change_category'
    },
    'back': {
        'text': '<<< назад',
        'callback_data': 'press_admin'
    },
}
