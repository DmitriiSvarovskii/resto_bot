from sqlalchemy.orm import relationship, Mapped  # noqa: F401
from typing import TYPE_CHECKING

from src.database import (
    Base, intpk, str_64,
    created_at, updated_at,
    deleted_at, deleted_flag
)

if TYPE_CHECKING:
    from src.models import Product  # noqa: F401


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
