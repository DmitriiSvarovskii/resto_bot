from pydantic import BaseModel, ConfigDict
from typing import List


class SalesSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    quantity: int
    unit_price: int


class SalesSummaryList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_items: List[SalesSummary]
    total_price: float


class OrderList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_price: float


class DeliveryReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    delivery_area: str
    delivery_count: int
    total_sales: float
