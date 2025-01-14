from sqlalchemy import select, func

from src.repositories.utils import get_free_rooms
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsModel
from src.models.hotels import HotelModel
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepositories):
    model = HotelModel
    schema = Hotel

    async def get_free_hotels(
            self, date_from, date_to, title, limit, offset, location):
        free_ids_rooms = get_free_rooms(date_from=date_from, date_to=date_to)
        free_hotels_ids = (
            select(RoomsModel.hotel_id).
            select_from(RoomsModel).
            filter(RoomsModel.id.in_(free_ids_rooms)))
        if title:
            free_hotels_ids = free_hotels_ids.filter(
                func.lower(HotelModel.title).contains(title.lstrip().lower()))
        if location:
            free_hotels_ids = free_hotels_ids.filter(
                func.lower(
                    HotelModel.location).contains(location.lstrip().lower()))
        free_hotels_ids = free_hotels_ids.limit(limit).offset(offset)
        return await self.get_filtred(HotelModel.id.in_(free_hotels_ids))
