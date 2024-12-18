from fastapi import Query, APIRouter

from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepositories
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Локация"),
):
    per_page = pagination.per_page or 2
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1))


@router.get("/{hotel_id}", summary="Отель")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_one(id=hotel_id)


@router.post("", summary="Добавлениe отеля")
async def hotel_post(hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepositories(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновление отеля")
async def hotel_put(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(
            hotel_data,
            id=hotel_id)
        await session.commit()
        return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
async def hotel_patch(hotel_data: HotelPatch, hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(
            hotel_data,
            exclude_unset=True,
            id=hotel_id)
        await session.commit()
        return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def hotel_delete(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepositories(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "OK"}
