from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    resourse: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    admin: Optional[bool] = False


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerCreate):
    pass


class CustomerInfo(CustomerBase):
    id: int
    is_active: bool


class CustomerAdResourse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_count: int


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
