from fastapi import APIRouter, Response, HTTPException

from src.schemas.users import UserRequestAdd, UserAdd
from src.repositories.users import UsersRepositories
from src.database import async_session_maker
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep
from src.api.dependencies import DBDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация")
async def register_user(db: DBDep, user_data: UserRequestAdd) -> dict:
    """Регистрация пользователя."""
    hashed_password = AuthService.pwd_context.hash(user_data.password)
    add_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    await db.users.add(add_data)
    await db.commit()
    return {"status": "OK"}


@router.post("/login", summary="Аутентификация")
async def login_user(db: DBDep, user_data: UserRequestAdd, response: Response):
    """Аутентификация пользователя."""
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    verify = AuthService().verify_password(
        user_data.password, user.hashed_password)
    if not verify:
        raise HTTPException(status_code=401, detail="Неверный пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    """Мои данные."""
    return await db.users.get_one(id=user_id)


@router.post("/logout")
async def logout_user(db: DBDep, response: Response) -> str:
    """Выход из системы."""
    response.delete_cookie("access_token")
    return "Вы вышли из системы"
