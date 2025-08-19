import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_ingredients(ac: AsyncClient):
    response = await ac.get("/ingredients")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_all_recipes(ac: AsyncClient):
    response = await ac.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_recipe_detail(ac: AsyncClient):
    response = await ac.get("/recipes/1")
    assert len(response.json()[0]["ingredients"]) == 3
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_recipe(ac: AsyncClient):
    response = await ac.post(
        "/recipes",
        json={
            "recipe_name": "Блины молочные",
            "cooking_time": 25,
            "views": 7,
            "recipe_description": "Тонкие блины на молоке",
            "ingredients": [
                {
                    "ingredient_id": 0,
                    "quantity": "Количество продукта"
                }
            ]
        },
    )
    assert response.json()["recipe_name"] == "Блины молочные"


@pytest.mark.asyncio
async def test_post_ingredient(ac: AsyncClient):
    response = await ac.post(
        "/ingredients",
        json={
            "ingredient_name": "Мука (Наименование)",
            "ingredient_description": "Пшеничная, высший сорт (Описание)"
        },
    )
    assert response.json()["ingredient_name"] == "Мука (Наименование)"
    assert response.json()["ingredient_description"] == "Пшеничная, выысший сорт (Описание)"
