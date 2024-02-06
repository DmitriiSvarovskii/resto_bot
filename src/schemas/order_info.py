from pydantic import BaseModel, ConfigDict
from typing import Optional


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
