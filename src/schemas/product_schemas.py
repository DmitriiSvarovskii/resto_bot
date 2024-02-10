from pydantic import BaseModel, ConfigDict


class ReadProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    description: str
    price: int
    availability: bool
