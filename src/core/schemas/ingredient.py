from pydantic import BaseModel, ConfigDict


class IngredientBase(BaseModel):
    ingredient_name: str = "Мука (Наименование)"
    ingredient_description: str = "Пшеничная, высший сорт. (Описание)"


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
