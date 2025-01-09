from datetime import date

from pydantic import BaseModel


class BookingAdd(BaseModel):
    rooms_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int
