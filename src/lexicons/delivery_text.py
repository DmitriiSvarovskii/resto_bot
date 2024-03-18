edit_delivery_dict: dict[str, str] = {
    'change_district_name': {
        'text': 'Изменить название ✏️',
        'callback_data': 'press_change_district_name'
    },
    'change_delivery_price': {
        'text': 'Изменить цену доставки ✏️',
        'callback_data': 'press_change_delivery_price'
    },
    'change_delivery_time': {
        'text': 'Изменить время доставки ✏️',
        'callback_data': 'press_change_delivery_time'
    },
    'add_new_district': {
        'text': 'Добавить новый район',
        'callback_data': 'press_add_new_district'
    },
    'delite_delivery': {
        'text': 'Удалить район ✖️',
        'callback_data': 'press_delite_delivery'
    },
    'back': {
        'text': '<<< назад',
        'callback_data': 'press_admin'
    },
}
