from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa: F401
from typing import TYPE_CHECKING

from src.database import Base, intpk, created_at

if TYPE_CHECKING:
    from src.models import Product, Order  # noqa: F401


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
