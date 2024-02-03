from pydantic import BaseModel, ConfigDict
from datetime import datetime, time
from typing import Optional


class GetStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    is_active: bool
    opening_time: Optional[datetime] = None
    closing_time: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    welcome_message_bot: Optional[str] = None
    sale_group: Optional[int] = None
    delivery_chat: Optional[int] = None
    order_chat: Optional[int] = None
    completed_orders_chat: Optional[int] = None
    canceled_orders_chat: Optional[int] = None
