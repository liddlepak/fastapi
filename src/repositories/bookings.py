from sqlalchemy import select

from src.repositories.base import BaseRepositories
from src.models.bookings import BookingsModel
from src.repositories.mappers.mappers import BookingMapper


class BookingRepositories(BaseRepositories):
    model = BookingsModel
    mapper = BookingMapper

    async def get_my_bookings(self, user_id):
        query = select(BookingsModel).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(
            booking) for booking in result.scalars().all()]
