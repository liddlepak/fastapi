from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.utils import get_free_rooms
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsModel
from src.schemas.rooms import Rooms, RoomsWithRels


class RoomsRepositories(BaseRepositories):
    model = RoomsModel
    schema = Rooms

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        free_ids_rooms = get_free_rooms(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to)
        query = (
            select(self.model).
            options(selectinload(RoomsModel.facilities)).
            filter(RoomsModel.id.in_(free_ids_rooms)))
        result = await self.session.execute(query)
        return [RoomsWithRels.model_validate(
            model, from_attributes=True) for model in result.unique().scalars().all()]

    async def get_one(self, **filters):
        query = (
            select(self.model).
            options(selectinload(RoomsModel.facilities)).
            filter_by(**filters))
        result = await self.session.execute(query)
        model = await self.get_object(result)
        return RoomsWithRels.model_validate(model, from_attributes=True)
