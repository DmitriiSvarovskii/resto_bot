from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class CartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int


class CartCreate(CartBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int


class CartGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    store_id: int


class CartItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: Optional[int] = None
    category_name_en: Optional[str] = None
    name_en: Optional[str] = None
    category_name_rus: Optional[str] = None
    name_rus: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[int] = None
    box_price: Optional[int] = None


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cart_items: List[CartItem] = None
    total_price: Optional[int] = None


class CartItemTotal(CartItem):
    model_config = ConfigDict(from_attributes=True)

    total_price: Optional[int] = None


class CartItemsOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
    unit_price: int


class CreateOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    store_id: int
    order_type_id: int


class CreateCustomerInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tg_user_name: Optional[str] = None
    table_number: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_comment: Optional[str] = None
