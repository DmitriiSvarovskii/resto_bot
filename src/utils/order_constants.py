from enum import Enum


class OrderStatus(Enum):
    NEW = {'id': 1, 'name_en': 'New', 'name_rus': 'Новый'}
    ACCEPTED = {'id': 2, 'name_en': 'Accepted', 'name_rus': 'Принят'}
    COMPLETED = {'id': 3, 'name_en': 'Completed', 'name_rus': 'Выполнен'}
    CANCELLED = {'id': 4, 'name_en': 'Cancelled', 'name_rus': 'Отменён'}
    COURIER_ASSIGNED = {
        'id': 5,
        'name_en': 'Assigned to courier',
        'name_rus': 'Передан курьеру'
    }
    READY_FOR_PICKUP = {
        'id': 6, 'name_en': 'Ready for pickup', 'name_rus': 'Готов к выдаче'}

    @classmethod
    def get_name_by_id(cls, target_id, language):
        for order_status in cls:
            if order_status.value['id'] == target_id:
                if language == 'ru':
                    return order_status.value['name_rus']
                else:
                    return order_status.value['name_en']
        return None

    @classmethod
    def get_id_by_name_enum(cls, name):
        for order_status in cls:
            if order_status.name == name:
                return order_status.value['id']
        return None

    @classmethod
    def get_name_by_name(cls, status_name, language):
        for order_status in cls:
            if order_status.name == status_name:
                if language == 'ru':
                    return order_status.value.get('name_rus')
                else:
                    return order_status.value.get('name_en')
        return None


class OrderTypes(Enum):
    TAKEAWAY = {'id': 1, 'name_rus': 'Самовывоз', 'name_en': 'Takeaway'}
    DELIVERY = {'id': 2, 'name_rus': 'Доставка', 'name_en': 'Delivery'}

    @classmethod
    def get_name_by_id(cls, target_id, language):
        for order_type in cls:
            if order_type.value['id'] == target_id:
                if language == 'ru':
                    return order_type.value['name_rus']
                else:
                    return order_type.value['name_en']
        return None

    @classmethod
    def get_id_by_name(cls, order_type_name):
        for order_type in cls:
            if order_type.value['name_rus'] or order_type.value['name_en'] == order_type_name:
                return order_type.value['id']
        return None


# Пример использования
name = OrderTypes.get_name_by_id(2, 'ru')
order_type_id = OrderTypes.get_id_by_name('Самовывоз')
# print(OrderTypes.TAKEAWAY.value['id'])
# print(type(OrderTypes.TAKEAWAY.value['id']))
print(OrderStatus.ACCEPTED.value['id'])
print(type(OrderStatus.ACCEPTED.value['id']))
# print(OrderTypes.TAKEAWAY.value.values('Самовывоз'))
# print('Самовывоз' is OrderTypes.TAKEAWAY.value.keys())
# values = OrderTypes.TAKEAWAY.value.values()
# if 'Самовывоз' in values:
#     print("'Самовывоз' найден!")
# else:
#     print("'Самовывоз' не найден.")
