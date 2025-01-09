from pydantic import BaseModel


class RoomsPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomsRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsRequest):
    id: int
    hotel_id: int


class RoomsAdd(RoomsRequest):
    hotel_id: int
