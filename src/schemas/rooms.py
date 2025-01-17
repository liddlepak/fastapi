from pydantic import BaseModel

from src.schemas.facilities import Facilities


class RoomsPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomsPatchWithFacilities(RoomsPatch):
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomsWithRels(Rooms):
    facilities: list[Facilities]


class RoomsPut(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomsRequestWithFacilities(RoomsPut):
    facilities_ids: list[int] | None = None
