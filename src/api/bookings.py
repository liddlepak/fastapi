from datetime import date

from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("", summary="Добавление бронирований")
async def add_bookings(
    room_id: int,
    date_from: date,
    date_to: date,
    db: DBDep,
    user_id: UserIdDep
):
    room = await db.rooms.get_one(id=room_id)
    price = room.price * (date_to - date_from).days
    booking_data = BookingAdd(
        rooms_id=room_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        price=price
    )
    booking = await db.bookings.add(booking_data)
    await db.commit()
    return {"booking": booking}
