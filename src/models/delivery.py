from sqlalchemy.orm import Mapped, relationship  # noqa: F401
from typing import TYPE_CHECKING

from src.database import Base, intpk, str_64

if TYPE_CHECKING:
    from src.models import Product  # noqa: F401


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[intpk]
    name: Mapped[str_64]
    delivery_time: Mapped[int]
    price: Mapped[int]

    # product: Mapped['Product'] = relationship(
    #     back_populates="carts")
