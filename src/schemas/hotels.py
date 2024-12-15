from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    location: str


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None


class HotelGet(BaseModel):
    title: Annotated[
        str | None, Query(default=None, ilike='', description="ID отеля")]
    location: Annotated[
        str | None, Query(default=None, description="Название отеля")]


HotelList = Annotated[HotelGet, Depends()]
