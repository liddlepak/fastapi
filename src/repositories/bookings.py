from sqlalchemy import select

from src.repositories.base import BaseRepositories
from src.models.bookings import BookingsModel
from src.schemas.bookings import Booking


class BookingRepositories(BaseRepositories):
    model = BookingsModel
    schema = Booking

    async def get_my_bookings(self, user_id):
        query = select(BookingsModel).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(
            bookings, from_attributes=True)for bookings in result.scalars().all()]
