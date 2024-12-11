from fastapi import Query, Path, APIRouter

from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},

]


@router.get("", summary="Список отелей")
def hotel_get(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[
        pagination.per_page * (pagination.page-1):][:pagination.per_page]


@router.delete("/{hotel_id}", summary="Удаление отеля")
def hotel_delete(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавлениe отеля")
def hotel_post(hotel_data: Hotel):
    global hotels
    hotel_id = len(hotels) + 1
    hotels.append(
        {"id": hotel_id,
         "title": hotel_data.title,
         "name": hotel_data.name})
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновление отеля")
def hotel_put(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

    return hotels


@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
def hotel_patch(hotel_data: HotelPatch,
                hotel_id: int = Path(description="Введите ID отеля")):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id and hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel["id"] == hotel_id and hotel_data.name:
            hotel["name"] = hotel_data.name
    return hotels
