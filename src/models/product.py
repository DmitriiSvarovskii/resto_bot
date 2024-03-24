from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship  # noqa: F401
from typing import TYPE_CHECKING

from src.db.database import (
    Base, intpk, str_64,
    str_256, created_at, updated_at,
    deleted_at, deleted_flag
)

if TYPE_CHECKING:
    from . import (  # noqa: F401
        Category,
        Cart,
        OrderDetail,
    )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[intpk]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"))
    name_rus: Mapped[str_64]
    description_rus: Mapped[str_256 | None]
    name_en: Mapped[str_64 | None]
    description_en: Mapped[str_256 | None]
    price: Mapped[int]
    price_box: Mapped[int | None]
    availability: Mapped[bool]
    popular: Mapped[bool] = mapped_column(server_default=text("false"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]

    # category: Mapped['Category'] = relationship(back_populates="products")
    # carts: Mapped['Cart'] = relationship(
    #     back_populates="product")
    # order_details: Mapped['OrderDetail'] = relationship(
    #     back_populates="product")
