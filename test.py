from typing import Optional
from pydantic import BaseModel


class CreateCustomerInfo(BaseModel):
    user_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    number_phone: Optional[str] = None
    guide: Optional[str] = None


data = {606825877: {'delivery_id': 7, 'number_phone': '1231231231',
                    'guide': 'Белый дом', 'latitude': 37.334601, 'longitude': -122.009199}}

# Получаем данные для пользователя с id 606825877
user_data = data.get(606825877, {})

# Создаем объект Pydantic класса, используя данные из словаря
customer_info = CreateCustomerInfo.model_validate(user_data)


