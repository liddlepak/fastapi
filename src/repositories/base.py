from typing import Optional, Any

from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from sqlalchemy.exc import MultipleResultsFound, NoResultFound


class BaseRepositories:
    model: Optional[Any] = None
    schema: Optional[Any] = None

    def __init__(self, session):
        self.session = session

    async def get_object(self, result):
        try:
            return result.scalars().one()
        except MultipleResultsFound:
            raise HTTPException(status_code=400, detail='Bad Request')
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Объект не найден")

    async def get_one(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        model = await self.get_object(result)
        return self.schema.model_validate(model, from_attributes=True)

    async def get_filtred(self, *filter, **filters):
        query = select(self.model).filter(*filter).filter_by(**filters)
        result = await self.session.execute(query)
        return [self.schema.model_validate(
            model, from_attributes=True) for model in result.scalars().all()]

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).  # type: ignore
            values(**data.model_dump()).
            returning(self.model))  # type: ignore
        print(add_data_stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(  # type: ignore
            model, from_attributes=True)

    async def edit(
            self, data: BaseModel, exclude_unset: bool = False, **filters
            ):
        update_stmt = (
            update(self.model).  # type: ignore
            filter_by(**filters).
            values(**data.model_dump(exclude_unset=exclude_unset)).
            returning(self.model.id))  # type: ignore
        print(update_stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(update_stmt)
        await self.get_object(result)

    async def delete(self, **filters):
        delete_stmt = (
            delete(self.model).
            filter_by(**filters).
            returning(self.model.id))
        result = await self.session.execute(delete_stmt)
        await self.get_object(result)
