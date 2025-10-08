from fastapi import APIRouter

from src.core.schemas.main_page import MainBase

main_route = APIRouter()


@main_route.get("/", tags=["Главная страница"], response_model=MainBase)
def main_page():
    return {"message": "Main page"}
