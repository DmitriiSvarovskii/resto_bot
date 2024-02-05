from sqlalchemy import BIGINT, text
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa: F401
from typing import TYPE_CHECKING

from src.database import (
    Base, intpk, created_at
)

if TYPE_CHECKING:
    from src.models import Order, OrderInfo  # noqa: F401


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    resourse: Mapped[str | None]
    admin: Mapped[bool | None] = mapped_column(server_default=text("false"))
    owner: Mapped[bool | None] = mapped_column(server_default=text("false"))
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    # orders: Mapped['Order'] = relationship(back_populates="customers")
    # order_info: Mapped['OrderInfo'] = relationship(
    #     back_populates="customers"
    # )
