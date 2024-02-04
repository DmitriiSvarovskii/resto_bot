from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa: F401
from typing import TYPE_CHECKING

from src.database import Base, intpk

if TYPE_CHECKING:
    from src.models import Product  # noqa: F401


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("customers.user_id", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]

    # product: Mapped['Product'] = relationship(
    #     back_populates="carts")
