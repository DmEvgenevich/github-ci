from typing import List

from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    recipe_name: str = "Блины молочные"
    cooking_time: int = 25
    views: int = 7
    recipe_description: str = "Тонкие блины на молоке. Нежные и вкусные."


class IngredientsInRecipe(BaseModel):
    ingredient_id: int
    quantity: str = "Количество продукта"


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientsInRecipe]


class RecipeRead(RecipeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int


class Ingredient(BaseModel):
    name: str
    description: str | None
    quantity: str | None


class RecipeDetail(BaseModel):
    id: int
    recipe_name: str
    cooking_time: int
    recipe_description: str
    views: int
    ingredients: List[Ingredient]
