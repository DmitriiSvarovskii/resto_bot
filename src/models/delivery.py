from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey

from src.db.database import (
    Base, intpk, str_64,
    created_at, updated_at,
    deleted_at, deleted_flag
)

if TYPE_CHECKING:
    from . import Product  # noqa: F401


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[intpk]
    store_id: Mapped[int | None] = mapped_column(
        ForeignKey("stories.id", ondelete="CASCADE"))
    name_rus: Mapped[str_64]
    name_en: Mapped[str_64 | None]
    delivery_time: Mapped[int]
    price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]

    # product: Mapped['Product'] = relationship(
    #     back_populates="carts")
