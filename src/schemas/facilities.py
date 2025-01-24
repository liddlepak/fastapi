from pydantic import BaseModel


class FacilitiesRequest(BaseModel):
    """Схема для запроса удобств."""
    title: str


class Facilities(FacilitiesRequest):
    """Схема удобств."""
    id: int


class RoomsFacilitiesAdd(BaseModel):
    """Схема для добавления удобств к номеру в БД."""
    room_id: int
    facility_id: int


class RoomsFacilities(RoomsFacilitiesAdd):
    """Схема связной модели удобств с номерами."""
    id: int
