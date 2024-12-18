from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from sqlalchemy.exc import MultipleResultsFound, NoResultFound


class BaseRepositories:
    model = None

    def __init__(self, session):
        self.session = session

    async def has_object(self, result):
        try:
            result.scalars().one()
        except MultipleResultsFound:
            raise HTTPException(status_code=400, detail='Bad Request')
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Not Found")

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        results = await self.session.execute(query)
        return results.scalars().all()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        results = await self.session.execute(query)
        return results.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump())
        print(add_data_stmt.
              compile(compile_kwargs={"literal_binds": True}))  # Дебаг код
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filters):
        update_data_stmt = (
            update(self.model).
            filter_by(**filters).
            values(**data.model_dump()).
            returning(self.model.id))
        result = await self.session.execute(update_data_stmt)
        await BaseRepositories.has_object(self, result)

    async def delete(self, **filters):
        delete_stmt = (
            delete(self.model).
            filter_by(**filters).
            returning(self.model.id))
        result = await self.session.execute(delete_stmt)
        await BaseRepositories.has_object(self, result)
