from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, intpk, created_at
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models import Product, Order


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    unit_price: Mapped[int]
    created_at: Mapped[created_at]

    # orders: Mapped['Order'] = relationship(back_populates="order_details")
    # product: Mapped['Product'] = relationship(back_populates="order_details")
