from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.utils import get_free_rooms
from src.repositories.base import BaseRepositories
from src.repositories.mappers.mappers import RoomMapper, RoomWithRelsMapper
from src.models.rooms import RoomsModel


class RoomsRepositories(BaseRepositories):
    """Репозиторий для номеров."""
    model = RoomsModel
    mapper = RoomMapper

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        """Получение номеров по фильтрам."""
        free_ids_rooms = get_free_rooms(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to)
        query = (
            select(self.model).
            options(selectinload(RoomsModel.facilities)).
            filter(RoomsModel.id.in_(free_ids_rooms)))
        result = await self.session.execute(query)
        return [RoomWithRelsMapper.map_to_domain_entity(
            model) for model in result.unique().scalars().all()]

    async def get_one(self, **filters):
        """Получение номера с удобствами."""
        query = (
            select(self.model).
            options(selectinload(RoomsModel.facilities)).
            filter_by(**filters))
        result = await self.session.execute(query)
        model = await self.get_object(result)
        return RoomWithRelsMapper.map_to_domain_entity(model)
