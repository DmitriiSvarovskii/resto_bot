from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    order_type: str

    order_status: Optional[str] = 'Новый'
    total_price: Optional[int] = None


class CreateOrderMessageId(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    message_id: int


class CreateOrderDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    product_id: int
    quantity: int
    unit_price: int


class CreateOrderInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    order_id: int
    order_comment: Optional[str] = None
    customer_phone: Optional[str] = None
    delivery_id: Optional[int] = None
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    delivery_comment: Optional[str] = None


class ReadOrderInfo(CreateOrderInfo):
    id: int


class ReadOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    order_type: str

    message_id: Optional[int] = None

    order_status: str
    total_price: int
    created_at: datetime


class ReadOrderList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_price: float


class ReadCustomerInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    admin: Optional[bool] = None
    owner: Optional[bool] = None
    first_name: Optional[str] = None
    username: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.first_name is None:
            self.first_name = "не указано"
        if self.username is None:
            self.username = "не указана"


class ReadDeliveryInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    delivery_village: Optional[str] = None
    number_phone: Optional[str] = None
    comment_for_delivery: Optional[str] = None


class ReadCustomer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    first_name: Optional[str] = None
    username: Optional[str] = None


class CreateOrderDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class ReadOrderDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_name: Optional[str] = None
    name: str
    quantity: int
    unit_price: int
