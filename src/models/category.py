from sqlalchemy.orm import relationship, Mapped, mapped_column  # noqa: F401
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING, List

from src.db.database import (
    Base, intpk, str_64,
    created_at, updated_at,
    deleted_at, deleted_flag
)

if TYPE_CHECKING:
    from . import Product  # noqa: F401


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    store_id: Mapped[int | None] = mapped_column(
        ForeignKey("stories.id", ondelete="CASCADE"))
    name_rus: Mapped[str_64]
    name_en: Mapped[str_64 | None]
    availability: Mapped[bool]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]

    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="category")
