from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepositories
from src.repositories.mappers.mappers import UserWithHashedPasswordMapper
from src.models.users import UserModel
from src.schemas.users import User


class UsersRepositories(BaseRepositories):
    """Репозиторий пользователя."""
    model = UserModel
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        """Получение пользователя."""
        query = select(UserModel).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            raise HTTPException(
                status_code=401,
                detail="Пользователь с такой почтой не существует")
        return UserWithHashedPasswordMapper.map_to_domain_entity(model)
