from src.repositories.base import BaseRepositories
from src.models.bookings import BookingsModel
from src.schemas.bookings import Booking


class BookingRepositories(BaseRepositories):
    model = BookingsModel
    schema = Booking
