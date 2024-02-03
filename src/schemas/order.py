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


class CreateOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    order_type: str

    order_status: Optional[str] = 'Новый'
    total_price: Optional[int] = None


class GetOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    order_type: str

    order_status: str
    total_price: int


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
