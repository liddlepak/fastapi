from sqlalchemy import select, func

from src.repositories.utils import get_free_rooms
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsModel
from src.models.hotels import HotelModel
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepositories):
    model = HotelModel
    schema = Hotel

    async def get_filtred(self, *filter, title, location, limit, offset):
        query = select(HotelModel).filter(*filter)
        if title:
            query = query.filter(
                func.lower(HotelModel.title).contains(title.lstrip().lower())
            )
        if location:
            query = query.filter(
                func.lower(
                    HotelModel.location).contains(location.lstrip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(
            model, from_attributes=True) for model in result.scalars().all()]

    async def get_free_hotels(
            self, date_from, date_to, title, limit, offset, location):
        free_ids_rooms = get_free_rooms(date_from=date_from, date_to=date_to)
        free_hotels_ids = (
            select(RoomsModel.hotel_id).
            select_from(RoomsModel).
            filter(RoomsModel.id.in_(free_ids_rooms)))
        return await self.get_filtred(
            HotelModel.id.in_(free_hotels_ids),
            title=title,
            location=location,
            limit=limit,
            offset=offset)
