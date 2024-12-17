from sqlalchemy import select, insert


class BaseRepositories:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        results = await self.session.execute(query)
        return results.scalars().all()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        results = await self.session.execute(query)
        return results.scalars().one_or_none()

    async def add(self, data):
        add_data_stmt = insert(self.model).values(**data.model_dump())
        print(add_data_stmt.
              compile(compile_kwargs={"literal_binds": True}))  # Дебаг код
        return await self.session.execute(add_data_stmt)
