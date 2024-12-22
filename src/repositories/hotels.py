from sqlalchemy import func, select

from src.repositories.base import BaseRepositories
from src.models.hotels import HotelModel
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepositories):
    model = HotelModel  # type: ignore
    schema = Hotel  # type: ignore

    async def get_all(self, title, location, limit, offset):
        query = select(HotelModel)
        if title:
            query = query.filter(
                func.lower(HotelModel.title).contains(title.lstrip().lower())
            )
        if location:
            query = query.filter(
                func.lower(
                    HotelModel.location).contains(location.lstrip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(model, from_attributes=True) for model in result.scalars().all()]
