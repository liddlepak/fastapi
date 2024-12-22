from src.repositories.base import BaseRepositories
from src.models.users import UserModel
from src.schemas.users import User


class UsersRepositories(BaseRepositories):
    model = UserModel
    schema = User