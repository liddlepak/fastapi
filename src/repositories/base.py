from typing import Optional, Any

from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from sqlalchemy.exc import MultipleResultsFound, NoResultFound


class BaseRepositories:
    """Базовый паттерн Репозиторий."""
    model: Optional[Any] = None
    mapper: Optional[Any] = None

    def __init__(self, session):
        """Инициализация сессиии."""
        self.session = session

    async def get_object(self, result) -> list:
        """Проверка на наличия объекта в БД."""
        try:
            return result.scalars().one()
        except MultipleResultsFound:
            raise HTTPException(status_code=400, detail='Bad Request')
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Объект не найден")

    async def get_one(self, **filters):
        """получение одного объекта из БД."""
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        model = await self.get_object(result)
        return self.mapper.map_to_domain_entity(model)

    async def get_filtred(self, *filter, **filters):
        """Получение списка объектов из БД по фильтрам."""
        query = select(self.model).filter(*filter).filter_by(**filters)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(
            model) for model in result.scalars().all()]

    async def add(self, data: BaseModel):
        """Добавление объекта в БД."""
        add_data_stmt = (
            insert(self.model).  # type: ignore
            values(**data.model_dump()).
            returning(self.model))  # type: ignore
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)  # type: ignore

    async def add_bulk(self, data: list[BaseModel]):
        """Добавление нескольких объектов в БД."""
        add_data_stmt = insert(self.model).values(  # type: ignore
            [item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(
            self, data: BaseModel, exclude_unset: bool = False, **filters
            ):
        """Редактирование объекта."""
        update_stmt = (
            update(self.model).  # type: ignore
            filter_by(**filters).
            values(**data.model_dump(exclude_unset=exclude_unset)).
            returning(self.model))  # type: ignore
        result = await self.session.execute(update_stmt)
        await self.get_object(result)

    async def delete(self, **filters):
        """Удаление объекта."""
        delete_stmt = (
            delete(self.model).
            filter_by(**filters).
            returning(self.model.id))
        result = await self.session.execute(delete_stmt)
        await self.get_object(result)

    async def delete_bulk(self, delete_ids):
        """Удаление нескольких объектов."""
        delete_stmt = (
            delete(self.model).
            filter(self.model.facility_id.in_(delete_ids))
        )
        await self.session.execute(delete_stmt)
