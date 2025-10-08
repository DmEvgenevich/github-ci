from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.ingredient import Ingredient
from src.core.schemas.ingredient import IngredientCreate


async def get_all_ingredients(
    session: AsyncSession,
) -> Sequence[Ingredient]:
    stmt = select(Ingredient).order_by(Ingredient.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_ingredient(
    session: AsyncSession,
    ingredient_create: IngredientCreate,
) -> Ingredient:
    ingredient = Ingredient(**ingredient_create.model_dump())
    session.add(ingredient)
    await session.commit()
    return ingredient
