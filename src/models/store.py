import datetime
from sqlalchemy import BIGINT, text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, intpk, str_4048


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[intpk]
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    opening_time: Mapped[datetime.time | None]
    closing_time: Mapped[datetime.time | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    welcome_message_bot: Mapped[str_4048 | None]
    sale_group: Mapped[int | None] = mapped_column(BIGINT)
    delivery_chat: Mapped[int | None] = mapped_column(BIGINT)
    order_chat: Mapped[int | None] = mapped_column(BIGINT)
    completed_orders_chat: Mapped[int | None] = mapped_column(BIGINT)
    canceled_orders_chat: Mapped[int | None] = mapped_column(BIGINT)
