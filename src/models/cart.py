from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, intpk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Product


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
