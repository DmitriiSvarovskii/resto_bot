from pydantic import BaseModel, ConfigDict
from typing import Optional


# class OrderBase(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     user_id: int
#     delivery_village: Optional[str] = None
#     delivery_address: Optional[str] = None
#     customer_name: Optional[str] = None
#     customer_phone: Optional[str] = None
#     customer_comment: Optional[str] = None


class CreateOrderDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    # order_type: int

    # order_status: Optional[str] = 'Новый'


class CreateCustomerInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    number_phone: Optional[str] = None
    guide: Optional[str] = None


class OrderDetailTest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_name: Optional[str] = None
    name: str
    quantity: int
    unit_price: int
