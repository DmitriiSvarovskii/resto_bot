from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class GetStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_active: bool
    opening_time: Optional[datetime] = None
    closing_time: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    welcome_message: Optional[str] = None
    sale_group: Optional[int] = None
    manager_group: Optional[int] = None
