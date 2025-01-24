from pydantic import BaseModel

from src.schemas.facilities import Facilities


class RoomsPatch(BaseModel):
    """Схема частичного редактирования номера."""
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomsPatchWithFacilities(RoomsPatch):
    """Схема редактирование номера с удобствами."""
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    """Схема добавление номера."""
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    """Схема номера."""
    id: int


class RoomsWithRels(Rooms):
    """Схема номера с удобствами."""
    facilities: list[Facilities]


class RoomsPut(BaseModel):
    """Схема редактирования номера."""
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomsRequestWithFacilities(RoomsPut):
    """Схема запроса на добавление номера с удобствами."""
    facilities_ids: list[int] | None = None
