from pydantic import BaseModel, ConfigDict


class DeliveryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price: int


class ReadDelivery(DeliveryBase):
    id: int


class ReadDeliveryReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    delivery_area: str
    delivery_count: int
    total_sales: float
