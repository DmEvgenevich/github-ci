from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.recipe import get_all_recipes, get_recipe_by_id, create_recipe
from core.models import db_helper
from core.schemas.recipe import RecipeCreate, RecipeDetail, RecipeRead


recipe_route = APIRouter()


@recipe_route.get(
    "/recipes", tags=["Список рецептов"], response_model=List[RecipeRead]
)
async def get_all_recipes(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ]
):
    recipes = await get_all_recipes(session=session)
    return recipes


@recipe_route.get(
    "/recipes/{recipe_id}",
    tags=["Детальное описание рецепта"],
    response_model=List[RecipeDetail],
)
async def get_recipe_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        recipe_id: int
):
    recipe = await get_recipe_by_id(
        session=session, recipe_id=recipe_id
    )
    return recipe


@recipe_route.post(
    "/recipes", tags=["Записать новый рецепт"], response_model=RecipeRead
)
async def add_new_recipe(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        recipe_data
):
    recipe = await create_recipe(
        session=session,
        recipe_create=recipe_data,
    )
    return recipe

