from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("", summary="Добавление бронирований")
async def add_bookings(
    data: BookingRequest,
    db: DBDep,
    user_id: UserIdDep
):
    room = await db.rooms.get_one(id=data.room_id)
    price = room.price * (data.date_to - data.date_from).days
    booking_data = BookingAdd(
        user_id=user_id,
        price=price,
        **data.model_dump())
    booking = await db.bookings.add(booking_data)
    await db.commit()
    return {"booking": booking}


@router.get("", summary="Список бронирований")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Список моих бронирований")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_my_bookings(user_id=user_id)
