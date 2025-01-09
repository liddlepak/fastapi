from fastapi import APIRouter, HTTPException
import sqlalchemy
import sqlalchemy.exc

from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsRequest
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepositories


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Список номеров")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_one(
            id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def add_room(room_data: RoomsRequest, hotel_id: int):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        try:
            room = await RoomsRepositories(session).add(
                _room_data)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=404, detail="Такого отеля не существует")
        await session.commit()
    return {"room": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение номера")
async def room_put(room_data: RoomsRequest, hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(
            room_data,
            hotel_id=hotel_id,
            id=room_id)
        await session.commit()
        return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
              summary="Частичное изменение номера")
async def room_patch(room_data: RoomsPatch, hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(
            room_data,
            hotel_id=hotel_id,
            id=room_id,
            exclude_unset=True)
        await session.commit()
        return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def room_delete(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepositories(session).delete(
            hotel_id=hotel_id,
            id=room_id)
        await session.commit()
        return {"status": "OK"}
