import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(ac: AsyncClient):
    # Тест проверки главной страницы
    response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_ingredients(ac: AsyncClient):
    # Тест проверки получения всех ингредиентов
    response = await ac.get("/ingredients")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_all_recipes(ac: AsyncClient):
    # Тест проверки получения всех рецептов
    response = await ac.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_recipe_detail(ac: AsyncClient):
    # Тест проверки получения детальной информации об рецепте
    response = await ac.get("/recipes/1")
    assert len(response.json()[0]["ingredients"]) == 3
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_recipe(ac: AsyncClient):
    # Тест проверки создания нового рецепта
    response = await ac.post(
        "/recipes",
        json={
            "recipe_name": "Created recipe",
            "cooking_time": 100,
            "views": 500,
            "recipe_description": "Тест пройден!",
            "ingredients": [{"ingredient_id": 1, "quantity": "test quantity"}],
        },
    )
    assert response.json()["recipe_name"] == "Created recipe"


@pytest.mark.asyncio
async def test_post_ingredient(ac: AsyncClient):
    # Тест проверки создания нового ингредиента
    response = await ac.post(
        "/ingredients",
        json={
            "ingredient_name": "name for test",
            "ingredient_description": "description for test",
        },
    )
    assert response.json()["ingredient_name"] == "name for test"
    assert response.json()["ingredient_description"] == "description for test"
