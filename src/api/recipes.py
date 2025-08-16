from fastapi import APIRouter

recipe_route = APIRouter()


@recipe_route.get("/recipes", tags=["Список рецептов"])
def get_all_recipes():
    return {"message": "Recipes"}
