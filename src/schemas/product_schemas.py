from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    name: str
    description: str
    price: int
    price_box: Optional[int] = None
    availability: bool


class ReadProduct(CreateProduct):
    id: int
