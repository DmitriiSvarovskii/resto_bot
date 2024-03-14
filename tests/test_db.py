import pytest

from src.db.database import Base, engine
from src.config import settings
from src.schemas.category_schemas import CreateCategory
from src.db import category_db
from src.models import Category


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    print(f'{settings.DB_NAME=}')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
async def categories():
    print(f'{settings.DB_NAME=}')
    print(f'{settings.MODE=}')
    assert settings.MODE == 'TEST'
    categories = CreateCategory(name="category_1", availability=True)

    return categories


@pytest.mark.asyncio
async def test_create_category(categories):
    stmt = await category_db.db_create_new_category(await categories)
    assert stmt['message'] == "Создана новая категория"
