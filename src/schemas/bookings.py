from datetime import date

from pydantic import BaseModel


class BookingRequest(BaseModel):
    """Схема запроса бронирований."""
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    """Схема для добавление брониваний в БД."""
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    """Схема бронирования."""
    id: int
