from pydantic import BaseModel


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


class RoomsPut(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomsRequestWithFacilities(RoomsPut):
    facilities_ids: list[int] | None = None
