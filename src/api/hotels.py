from fastapi import Path, APIRouter
from sqlalchemy import insert, select

from src.models.hotels import HotelModel
from src.schemas.hotels import Hotel,  HotelPatch, HotelList
from src.api.dependencies import PaginationDep
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
async def hotel_get(pagination: PaginationDep, hotel_data: HotelList):
    per_page = pagination.per_page or 2
    async with async_session_maker() as session:
        query = select(HotelModel)
        if hotel_data.title:
            query = query.filter(HotelModel.title.
                                 ilike(f'%{hotel_data.title}%'))
        if hotel_data.location:
            query = query.filter(HotelModel.location.
                                 ilike(f'%{hotel_data.location}%'))
        query = (query.
                 limit(per_page).
                 offset(per_page * (pagination.page-1))
                 )
        result = await session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}", summary="Удаление отеля")
def hotel_delete(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавлениe отеля")
async def hotel_post(hotel_data: Hotel):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelModel).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(
            compile_kwargs={"literal_binds": True}))  # Дебаг код
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


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
