ORDER_TYPES = {
    'takeaway': {'id': 1, 'name': 'Самовывоз'},
    'delivery': {'id': 2, 'name': 'Доставка'},
}

ORDER_STATUSES = {
    'new': {'id': 1, 'name': 'Новый'},
    'accepted': {'id': 2, 'name': 'Принят'},
    'completed': {'id': 3, 'name': 'Выполнен'},
    'cancelled': {'id': 4, 'name': 'Отменён'},
    'courier_assigned': {'id': 5, 'name': 'Передан курьеру'},
    'ready_for_pickup': {'id': 6, 'name': 'Готов к выдаче'},
}


async def get_status_name_by_id(status_id: int) -> str:
    for status_name, status_info in ORDER_STATUSES.items():
        if status_info['id'] == status_id:
            return status_info['name']

    raise ValueError(f"Status with id {status_id} not found in ORDER_STATUSES")


async def get_order_type_name_by_id(type_id: int) -> str:
    for type_name, type_info in ORDER_TYPES.items():
        if type_info['id'] == type_id:
            return type_info['name']

    raise ValueError(f"Order type with id {type_id} not found in ORDER_TYPES")
