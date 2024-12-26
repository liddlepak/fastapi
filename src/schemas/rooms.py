from pydantic import BaseModel


class RoomsPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomsPut(BaseModel):
    title: str
    description: str
    price: int
    quantity: int


class Rooms(RoomsPatch):
    id: int


class RoomsAdd(RoomsPut):
    hotel_id: int
