from typing import Annotated

from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    """Реализация пагинации."""
    page: Annotated[
        int, Query(default=1, ge=1, description='Страница')]
    per_page: Annotated[
        int | None, Query(
            default=None, ge=1, lt=30, description='Отелей на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    """Получение токена."""
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    """Получение id текущего пользователя."""
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    """Получение репозитория БД."""
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
