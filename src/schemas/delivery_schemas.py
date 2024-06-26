from pydantic import BaseModel, ConfigDict


class DeliveryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name_rus: str
    name_en: str
    price: int


class ReadDelivery(DeliveryBase):
    id: int


class ReadDeliveryReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    delivery_area: str
    delivery_count: int
    total_sales: float


class CreateDelivery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
    name_rus: str
    name_en: str
    delivery_time: int
    price: int
