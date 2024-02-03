from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    resourse: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerInfo(CustomerBase):
    id: int
    is_active: bool


class CustomerAdResourse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # resourse: str
    customer_count: int
