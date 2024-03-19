from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    name: str
    description: str
    price: int
    price_box: Optional[int] = 0
    availability: bool
    popular: Optional[bool] = False


class ReadProduct(CreateProduct):
    id: int


class UpdateProduct(CreateProduct):
    pass
