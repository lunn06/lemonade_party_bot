import random
from collections import deque

from sqlalchemy import ForeignKey, TEXT
from sqlalchemy.dialects.postgresql import TIMESTAMP, BIGINT, BOOLEAN, INTEGER, INTERVAL
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from bot.database.base import Base


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


lottery = [i for i in range(100_000, 110_000)]
random.shuffle(lottery)
lottery_deque = deque(lottery)


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True
    )
    registered_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=utcnow()
    )
    user_name: Mapped[str] = mapped_column(
        TEXT,
    )
    lottery: Mapped[int] = mapped_column(
        INTEGER,
        unique=True,
        default=lottery_deque.pop
    )
    points: Mapped[int] = mapped_column(
        INTEGER,
        default=0
    )
    quest_time: Mapped[int] = mapped_column(
        INTERVAL,
        nullable=True,
    )

    # async def quest_time(self, session: AsyncSession):
    #     # min_completed_at = session.query(func.min(UserStations.completed_at)).filter(
    #     #     UserStations.telegram_id == self.telegram_id).scalar()
    #     # max_completed_at = session.query(func.max(UserStations.completed_at)).filter(
    #     #     UserStations.telegram_id == self.telegram_id).scalar()
    #     min_stmt = select(func.min(UserStations.completed_at)).filter(
    #         UserStations.telegram_id == self.telegram_id)
    #     max_stmt = select(func.max(UserStations.completed_at)).filter(
    #         UserStations.telegram_id == self.telegram_id)
    #
    #     min_completed_at = await session.scalar(min_stmt)
    #     max_completed_at = await session.scalar(max_stmt)
    #
    #     return max_completed_at - min_completed_at
    # user_stations: Mapped[list["UserStations"]] = relationship(
    #     back_populates="telegram_user",
    #     cascade="all, delete-orphan"
    # )


class Station(Base):
    __tablename__ = "stations"
    station_name: Mapped[str] = mapped_column(
        TEXT,
        primary_key=True
    )
    coast: Mapped[str] = mapped_column(
        INTEGER
    )
    is_special: Mapped[bool] = mapped_column(
        BOOLEAN,
        default=False
    ),
    # user_stations: Mapped[list["UserStations"]] = relationship(
    #     back_populates="telegram_user",
    #     cascade="all, delete-orphan"
    # )


class UserStations(Base):
    __tablename__ = "user_stations"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"),
        primary_key=True
    )
    station_name: Mapped[str] = mapped_column(
        ForeignKey("stations.station_name"),
        primary_key=True
    )
    completed_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=utcnow()
    )
    # telegram_user: Mapped["User"] = relationship(
    #     back_populates="user_stations"
    # )
    # station: Mapped["Station"] = relationship(
    #     back_populates="stations"
    # )
