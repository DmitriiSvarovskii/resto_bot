from sqlalchemy.orm import Mapped, relationship

from src.database import Base, intpk, str_64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Product


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[intpk]
    name: Mapped[str_64]
    delivery_time: Mapped[int]
    price: Mapped[int]

    # product: Mapped['Product'] = relationship(
    #     back_populates="carts")
