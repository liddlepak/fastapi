from src.repositories.base import BaseRepositories
from src.models.facilities import FacilitiesModel, RoomFacilitiesModel
from src.schemas.facilities import Facilities, RoomsFacilities


class FacilitiesRepositories(BaseRepositories):
    model = FacilitiesModel
    schema = Facilities


class RoomsFacilitiesRepositories(BaseRepositories):
    model = RoomFacilitiesModel
    schema = RoomsFacilities
