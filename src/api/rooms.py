from datetime import date

from fastapi import APIRouter, HTTPException, Query
import sqlalchemy.exc

from src.repositories.utils import check_empty_request
from src.schemas.facilities import RoomsFacilitiesAdd
from src.api.dependencies import DBDep
from src.schemas.rooms import (
    RoomsAdd,
    RoomsPatch,
    RoomsRequestWithFacilities,
    RoomsPatchWithFacilities,
    RoomsPut,
)


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Список номеров")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-01-01"),
    date_to: date = Query(example="2025-01-16"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def add_room(
    room_data: RoomsRequestWithFacilities, hotel_id: int, db: DBDep
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=404, detail="Такого отеля не существует")
    facilities_ids = room_data.facilities_ids
    if facilities_ids is not None:
        facilities_data = [
            RoomsFacilitiesAdd(
                room_id=room.id, facility_id=id) for id in facilities_ids]
        await db.room_facilities.add_bulk(facilities_data)
    await db.commit()
    return {"room": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение номера")
async def room_put(
    room_data: RoomsRequestWithFacilities,
    hotel_id: int, room_id: int, db: DBDep
):
    update_room_data = RoomsPut(**room_data.model_dump())
    await db.room_facilities.edit_facility(room_data.facilities_ids, room_id)
    await db.rooms.edit(update_room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение")
async def room_patch(
    room_data: RoomsPatchWithFacilities, hotel_id: int, room_id: int, db: DBDep
):
    update_room_data = RoomsPatch(**room_data.model_dump(exclude_unset=True))
    if check_empty_request(update_room_data):
        await db.rooms.edit(
            update_room_data,
            hotel_id=hotel_id,
            id=room_id,
            exclude_unset=True)
    await db.room_facilities.edit_facility(room_data.facilities_ids, room_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def room_delete(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
