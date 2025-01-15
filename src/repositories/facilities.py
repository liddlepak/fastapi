from src.repositories.base import BaseRepositories
from src.models.facilities import FacilitiesModel
from src.schemas.facilities import Facilities


class FacilitiesRepositories(BaseRepositories):
    model = FacilitiesModel
    schema = Facilities