from pydantic import BaseModel


class FacilitiesRequest(BaseModel):
    title: str


class Facilities(FacilitiesRequest):
    id: int
