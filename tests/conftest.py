from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from src.core.models import db_helper
from src.core.models.base import Base
from src.core.models.ingredient import Ingredient
from src.core.models.ingredient_in_recipe import IngredientsInRecipe
from src.core.models.recipe import Recipe
from src.main import main_app

DATABASE_URL_TEST = "postgresql+asyncpg://test:test@localhost:5432/test"
engine_test = create_async_engine(
    DATABASE_URL_TEST, poolclass=NullPool, echo=True
)
async_session = async_sessionmaker(bind=engine_test, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


main_app.dependency_overrides[db_helper.session_getter] = (
    override_get_async_session
)
client = TestClient(main_app)

ingredients = [
    {
        "ingredient_name": "Test ingredient 1",
        "ingredient_description": "Test ingredient description 1",
    },
    {
        "ingredient_name": "Test ingredient 2",
        "ingredient_description": "Test ingredient description 2",
    },
    {
        "ingredient_name": "Test ingredient 3",
        "ingredient_description": "Test ingredient description 3",
    },
]
recipes = [
    {
        "recipe_name": "Test recipe 1",
        "cooking_time": 25,
        "recipe_description": "Test recipe description 1",
    },
    {
        "recipe_name": "Test recipe 2",
        "cooking_time": 50,
        "recipe_description": "Test recipe description 2",
    },
]
ingredients_to_recipes = [
    # 1 рецепт
    {"recipe_id": 1, "ingredient_id": 1, "quantity": "i1 test r1"},
    {"recipe_id": 1, "ingredient_id": 2, "quantity": "i2 test r1"},
    {"recipe_id": 1, "ingredient_id": 3, "quantity": "i3 test r1"},
    {"recipe_id": 2, "ingredient_id": 3, "quantity": "i3 test r2"},
    {"recipe_id": 2, "ingredient_id": 2, "quantity": "i2 test r2"},
]


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        await conn.execute(insert(Ingredient), ingredients)
        await conn.execute(insert(Recipe), recipes)
        await conn.execute(insert(IngredientsInRecipe), ingredients_to_recipes)

        await conn.commit()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as async_test_client:
        yield async_test_client
