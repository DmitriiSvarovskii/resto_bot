from sqlalchemy.orm import relationship, Mapped
from src.database import (
    Base, intpk, str_64,
    created_at, updated_at,
    deleted_at, deleted_flag
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Product


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]

    # products: Mapped['Product'] = relationship(back_populates="category")
