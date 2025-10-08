from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class IngredientsInRecipe(Base):
    """
    Класс, описывающий связь рецептов, ингредиентов и их количества
    """

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[str | None] = mapped_column(String(100))

    def __repr__(self):
        return (
            f"IngredientsInRecipe(recipe_id={self.recipe_id}, "
            f"ingredient_id={self.ingredient_id}, quantity={self.quantity})"
        )
