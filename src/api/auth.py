from fastapi import APIRouter, Response, HTTPException

from src.schemas.users import UserRequestAdd, UserAdd
from src.repositories.users import UsersRepositories
from src.database import async_session_maker
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация")
async def register_user(user_data: UserRequestAdd):
    hashed_password = AuthService.pwd_context.hash(user_data.password)
    add_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepositories(session).add(add_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login", summary="Авторизация")
async def login_user(user_data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepositories(
            session).get_user_with_hashed_password(email=user_data.email)
        verify = AuthService().verify_password(
            user_data.password, user.hashed_password)
        if not verify:
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
