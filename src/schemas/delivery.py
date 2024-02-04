from pydantic import BaseModel, ConfigDict


class DeliveryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price: int


class ReadDelivery(DeliveryBase):
    id: int
