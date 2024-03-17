from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateOrderDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class CreateCustomerInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    number_phone: Optional[str] = None
    guide: Optional[str] = None


class ReadOrderDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_name: Optional[str] = None
    name: str
    quantity: int
    unit_price: int
