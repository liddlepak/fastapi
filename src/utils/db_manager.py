from src.repositories.hotels import HotelsRepositories
from src.repositories.rooms import RoomsRepositories
from src.repositories.users import UsersRepositories
from src.repositories.bookings import BookingRepositories


class DBManager():
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepositories(self.session)
        self.rooms = RoomsRepositories(self.session)
        self.users = UsersRepositories(self.session)
        self.bookings = BookingRepositories(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
