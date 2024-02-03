import datetime
from typing import Annotated, AsyncGenerator
from sqlalchemy import MetaData, String, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.pool import NullPool
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

metadata = MetaData()


engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


str_64 = Annotated[str, 64]
str_256 = Annotated[str, 256]
str_4048 = Annotated[str, 4048]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_64: String(64),
        str_256: String(256),
        str_4048: String(4048),

    }


intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
is_active = Annotated[bool, mapped_column(server_default=text("true"))]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]
deleted_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("null"),
    onupdate=datetime.datetime.utcnow, nullable=True
)]
deleted_flag = Annotated[bool, mapped_column(server_default=text("false"))]
