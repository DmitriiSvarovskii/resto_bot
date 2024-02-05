from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa: F401
from typing import TYPE_CHECKING

from src.database import Base, intpk

if TYPE_CHECKING:
    from src.models import Order  # noqa: F401


class OrderInfo(Base):
    __tablename__ = "orders_info"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("customers.user_id", ondelete="CASCADE")
    )
    order_comment: Mapped[str | None]
    customer_phone: Mapped[str | None]
    delivery_id: Mapped[int | None] = mapped_column(
        ForeignKey("deliveries.id", ondelete="CASCADE")
    )
    delivery_latitude: Mapped[float | None]
    delivery_longitude: Mapped[float | None]
    delivery_comment: Mapped[str | None]

    # orders: Mapped['Order'] = relationship(
    #     back_populates="order_nfo")
    # customers: Mapped['Order'] = relationship(
    #     back_populates="order_info")
