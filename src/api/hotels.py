from datetime import date
from fastapi import Query, APIRouter

from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2025-01-01"),
    date_to: date = Query(example="2025-01-16"),
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Локация"),
):
    per_page = pagination.per_page or 2
    return await db.hotels.get_free_hotels(
        date_from=date_from, date_to=date_to,
        title=title, location=location,
        limit=per_page, offset=per_page * (pagination.page - 1))


@router.get("/{hotel_id}", summary="Отель")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one(id=hotel_id)


@router.post("", summary="Добавлениe отеля")
async def hotel_post(hotel_data: HotelAdd, db: DBDep):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновление отеля")
async def hotel_put(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(
        hotel_data,
        id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
async def hotel_patch(hotel_data: HotelPatch, hotel_id: int, db: DBDep):
    await db.hotels.edit(
        hotel_data,
        exclude_unset=True,
        id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def hotel_delete(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
