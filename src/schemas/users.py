from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    """Схема запроса добавление юзера в БД."""
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    """Схема добавление юзера в БД с хэш-паролем."""
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    """Схема юзера."""
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    """Схема юзера с хэш-паролем."""
    hashed_password: str
