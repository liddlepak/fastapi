from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base


class BookingsModel(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rooms_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date] = mapped_column()
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_to - self.date_from).days
