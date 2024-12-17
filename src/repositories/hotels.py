from sqlalchemy import func, select

from src.repositories.base import BaseRepositories
from src.models.hotels import HotelModel


class HotelsRepositories(BaseRepositories):
    model = HotelModel

    async def get_all(self, title, location, limit, offset):
        query = select(HotelModel)
        if title:
            query = query.filter(
                func.lower(HotelModel.title).contains(
                    title.lstrip().lower()))
        if location:
            query = query.filter(
                func.lower(HotelModel.location).contains(
                    location.lstrip().lower()))
        query = query.limit(limit).offset(offset)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()
