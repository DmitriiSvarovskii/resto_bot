import datetime
from sqlalchemy import BIGINT, text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base, intpk, str_4048


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[intpk]
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    opening_time: Mapped[datetime.time | None]
    closing_time: Mapped[datetime.time | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    sale_group: Mapped[int | None] = mapped_column(BIGINT)
    manager_group: Mapped[int | None] = mapped_column(BIGINT)
    welcome_message: Mapped[str_4048 | None]
