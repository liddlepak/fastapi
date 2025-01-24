from pydantic import BaseModel


class HotelAdd(BaseModel):
    """Схема добавление отеля в БД."""
    title: str
    location: str


class Hotel(HotelAdd):
    """Схема отеля."""
    id: int


class HotelPatch(BaseModel):
    """Схема редактирования отеля."""
    title: str | None = None
    location: str | None = None
