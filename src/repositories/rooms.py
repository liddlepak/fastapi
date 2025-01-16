from src.repositories.utils import get_free_rooms
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsModel
from src.schemas.rooms import Rooms


class RoomsRepositories(BaseRepositories):
    model = RoomsModel
    schema = Rooms

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        free_ids_rooms = get_free_rooms(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )
        return await self.get_filtred(RoomsModel.id.in_(free_ids_rooms))

