from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud import ingredient
from src.core.models import db_helper
from src.core.schemas.ingredient import IngredientCreate, IngredientRead

ingredient_route = APIRouter()


@ingredient_route.get(
    "/ingredients",
    tags=["Вывести спсиок ингредиентов"],
    response_model=List[IngredientRead],
)
async def get_all_ingredients(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ]
):
    ingredients = await ingredient.get_all_ingredients(session=session)
    return ingredients


@ingredient_route.post(
    "/ingredients",
    tags=["Добавить новый ингредиент"],
    response_model=IngredientRead,
)
async def add_new_ingredients(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        ingredient_data: IngredientCreate,
):
    ingredients = await ingredient.create_ingredient(
        session=session,
        ingredient_create=ingredient_data,
    )
    return ingredients
