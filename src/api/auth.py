from fastapi import APIRouter

from src.schemas.users import UserRequestAdd, UserAdd
from src.repositories.users import UsersRepositories
from src.database import async_session_maker
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", summary="Регистрация")
async def register_user(user_data: UserRequestAdd):
    hashed_password = pwd_context.hash(user_data.password)
    add_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepositories(session).add(add_data)
        await session.commit() 
    return {"status": "OK"}
