from pydantic import BaseModel


class FacilitiesRequest(BaseModel):
    title: str


class Facilities(FacilitiesRequest):
    id: int


class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilities(RoomsFacilitiesAdd):
    id: int
