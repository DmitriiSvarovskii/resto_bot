from src.callbacks import StoreAdminCbData


def create_edit_delivery_btn(
    store_id: int
) -> dict[str, dict[str, str]]:
    return {
        'change_district_name': {
            'text': 'Изменить название ✏️',

            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='change-district-name'
            ).pack()
        },
        'change_delivery_price': {
            'text': 'Изменить цену доставки ✏️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='change-delivery-price'
            ).pack()
        },
        'change_delivery_time': {
            'text': 'Изменить время доставки ✏️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='change-delivery-time'
            ).pack()
        },
        'add_new_district': {
            'text': 'Добавить новый район',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='add-new-district'
            ).pack()
        },
        'delite_delivery': {
            'text': 'Удалить район ✖️',
            'callback_data': StoreAdminCbData(
                store_id=store_id,
                type_press='delite-delivery'
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
