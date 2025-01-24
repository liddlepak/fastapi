from sqlalchemy import select, func

from src.repositories.utils import get_free_rooms
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsModel
from src.models.hotels import HotelModel
from src.repositories.mappers.mappers import HotelMapper


class HotelsRepositories(BaseRepositories):
    """Репозиторий для отелей."""
    model = HotelModel
    mapper = HotelMapper

    async def get_free_hotels(
            self, date_from, date_to, title, limit, offset, location
            ):
        """Получение свободных отелей."""
        free_ids_rooms = get_free_rooms(date_from=date_from, date_to=date_to)
        free_hotels_ids = (
            select(RoomsModel.hotel_id).
            select_from(RoomsModel).
            filter(RoomsModel.id.in_(free_ids_rooms)))

        query = select(HotelModel).filter(HotelModel.id.in_(free_hotels_ids))
        if title:
            query = query.filter(
                func.lower(HotelModel.title).contains(title.lstrip().lower()))
        if location:
            query = query.filter(
                func.lower(
                    HotelModel.location).contains(location.lstrip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(
            model) for model in result.scalars().all()]
