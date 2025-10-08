from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.ingredient import Ingredient
from src.core.models.ingredient_in_recipe import IngredientsInRecipe
from src.core.models.recipe import Recipe
from src.core.schemas.recipe import RecipeCreate


async def get_all_recipes(
    session: AsyncSession,
) -> Sequence[Recipe]:
    stmt = select(Recipe).order_by(Recipe.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_recipe_by_id(session: AsyncSession, recipe_id: int):
    result = await session.execute(
        select(Recipe).filter(Recipe.id == recipe_id)
    )
    result_2 = await session.execute(
        select(
            IngredientsInRecipe.quantity,
            Ingredient.ingredient_name,
            Ingredient.ingredient_description,
        )
        .join(Ingredient, Ingredient.id == IngredientsInRecipe.ingredient_id)
        .where(IngredientsInRecipe.recipe_id == recipe_id)
    )

    recipe = result.scalars().one()
    ingredients = result_2.fetchall()

    recipe.views += 1
    await session.commit()

    recipe_with_ingredients = [
        {
            "id": recipe.id,
            "recipe_name": recipe.recipe_name,
            "cooking_time": recipe.cooking_time,
            "recipe_description": recipe.recipe_description,
            "views": recipe.views,
            "ingredients": [
                {
                    "name": i.ingredient_name,
                    "description": i.ingredient_description,
                    "quantity": i.quantity,
                }
                for i in ingredients
            ],
        },
    ]
    return recipe_with_ingredients


async def create_recipe(
    session: AsyncSession,
    recipe_create: RecipeCreate,
) -> Recipe:
    data = recipe_create.model_dump()
    recipe = Recipe(
        recipe_name=data["recipe_name"],
        cooking_time=data["cooking_time"],
        views=data["views"],
        recipe_description=data["recipe_description"],
    )
    session.add(recipe)
    await session.flush()
    ingredients_in_recipe = []
    for item in data["ingredients"]:
        ingredients_in_recipe.append(
            IngredientsInRecipe(
                recipe_id=recipe.id,
                ingredient_id=item["ingredient_id"],
                quantity=item["quantity"],
            )
        )
    session.add_all(ingredients_in_recipe)
    await session.commit()
    return recipe
