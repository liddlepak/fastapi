from sqlalchemy import insert

from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsModel
from src.schemas.rooms import Rooms


class RoomsRepositories(BaseRepositories):
    model = RoomsModel
    schema = Rooms
