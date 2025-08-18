from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.ingredient import get_all_ingredients, create_ingredient
from core.models import db_helper
from core.schemas.ingredient import IngredientCreate, IngredientRead

ingredient_route = APIRouter()


@ingredient_route.get(
    "/ingredients",
    tags=["Вывести спсиок ингредиентов"],
    response_model=List[IngredientRead],
)
async def get_all_ingredients(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    ingredients = await get_all_ingredients(session=session)
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
    ingredient = await create_ingredient(
        session=session,
        ingredient_create=ingredient_data,
    )
    return ingredient
