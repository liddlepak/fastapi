from fastapi import Path, Query, APIRouter

from src.models.hotels import HotelModel
from src.schemas.hotels import Hotel,  HotelPatch
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepositories
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
async def hotel_get(
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
            offset=per_page * (pagination.page - 1)
        )


@router.delete("/{hotel_id}", summary="Удаление отеля")
def hotel_delete(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавлениe отеля")
async def hotel_post(hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepositories(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel_data}


@router.put("/{hotel_id}", summary="Обновление отеля")
def hotel_put(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.location

    return hotels


@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
def hotel_patch(
    hotel_data: HotelPatch,
    hotel_id: int = Path(description="ID отеля")
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id and hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel["id"] == hotel_id and hotel_data.location:
            hotel["name"] = hotel_data.location
    return hotels
