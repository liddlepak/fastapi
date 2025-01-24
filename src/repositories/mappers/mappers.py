from src.repositories.mappers.base import DataMapper
from src.models.bookings import BookingsModel
from src.models.facilities import FacilitiesModel
from src.models.rooms import RoomsModel
from src.models.users import UserModel
from src.models.hotels import HotelModel
from src.schemas.bookings import Booking
from src.schemas.facilities import Facilities
from src.schemas.rooms import Rooms, RoomsWithRels
from src.schemas.users import User, UserWithHashedPassword
from src.schemas.hotels import Hotel


class HotelMapper(DataMapper):
    """Реализация паттерна для отелей."""
    db_model = HotelModel
    schema = Hotel


class RoomMapper(DataMapper):
    """Реализация паттерна для номеров."""
    db_model = RoomsModel
    schema = Rooms


class RoomWithRelsMapper(DataMapper):
    """Реализация паттерна для номеров с удоствами."""
    db_model = RoomsModel
    schema = RoomsWithRels


class BookingMapper(DataMapper):
    """Реализация паттерна для бронирований."""
    db_model = BookingsModel
    schema = Booking


class FacilityMapper(DataMapper):
    """Реализация паттерна для удобств."""
    db_model = FacilitiesModel
    schema = Facilities


class UserMapper(DataMapper):
    """Реализация паттерна для пользователей."""
    db_model = UserModel
    schema = User


class UserWithHashedPasswordMapper(DataMapper):
    """Реализация паттерна для хэширования паролей"""
    db_model = UserModel
    schema = UserWithHashedPassword
