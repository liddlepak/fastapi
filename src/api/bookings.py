from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("", summary="Список бронирований")
@cache(expire=30)
async def get_all_bookings(db: DBDep) -> list:
    """Список бронирований."""
    return await db.bookings.get_filtred()


@router.get("/me", summary="Список моих бронирований")
@cache(expire=30)
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> list:
    """Получение бронирований текущего пользователя."""
    return await db.bookings.get_my_bookings(user_id=user_id)


@router.post("", summary="Добавление бронирований")
async def add_bookings(data: BookingRequest, db: DBDep, user_id: UserIdDep):
    """Функция для добавления бронирования."""
    room = await db.rooms.get_one(id=data.room_id)
    price = room.price * (data.date_to - data.date_from).days
    booking_data = BookingAdd(
        user_id=user_id,
        price=price,
        **data.model_dump())
    booking = await db.bookings.add(booking_data)
    await db.commit()
    return {"booking": booking}
