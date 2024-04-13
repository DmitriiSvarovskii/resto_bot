from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa: F401
from typing import TYPE_CHECKING, List  # noqa: F401

from src.db.database import Base, intpk, created_at, str_64, updated_at

if TYPE_CHECKING:
    from . import OrderInfo, OrderDetail, Customer  # noqa: F401


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customers.user_id",
            ondelete="CASCADE"
        )
    )
    order_type: Mapped[str_64]
    order_status: Mapped[str_64]
    total_price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # order_nfo: Mapped[List['OrderInfo']] = relationship(
    #     back_populates="orders")
    # customers: Mapped['Customer'] = relationship(back_populates="orders")
    # order_details: Mapped['OrderDetail'] = relationship(
    #     back_populates="orders")


class OrderMessageId(Base):
    __tablename__ = "order_messages_id"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE")
    )
    message_id: Mapped[int | None]
    created_at: Mapped[created_at]
