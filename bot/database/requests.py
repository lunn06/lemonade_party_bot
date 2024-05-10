from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_reader import Config
from bot.database.models import User, UserStations, Station


async def prepare_database(session: AsyncSession, config: Config) -> None:
    for st in config.stations_list:
        coast = config.usual_station_points
        is_special = False
        if st in config.star_stations:
            is_special = True
            coast = config.star_station_points
        await ensure_station(
            session,
            station_name=st,
            coast=coast,
            is_special=is_special
        )


async def ensure_station(session: AsyncSession, station_name: str, coast: int, is_special: bool) -> None:
    stmt = select(Station).where(Station.station_name == station_name)
    existing_station = await session.scalar(stmt)

    if existing_station is not None:
        return

    station = Station(
        station_name=station_name,
        coast=coast,
        is_special=is_special
    )

    session.add(station)

    await session.commit()


async def get_top_users(session: AsyncSession, limit: int = 100) -> list[User]:
    stmt = select(User).order_by(User.points).limit(limit)
    res = await session.execute(stmt)
    return [r[0] for r in res]

    # if res is None:
    #     return []
    # if isinstance(res, User):
    #     return [res, ]
    # return list(res)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """
    Получает пользователя по его айди.
    :param session: объект AsyncSession
    :param user_id: айди пользователя
    :return: объект RegisteredUser или None
    """
    stmt = select(User).where(User.telegram_id == user_id)
    return await session.scalar(stmt)


async def ensure_user(session: AsyncSession, user_id: int, user_name: str) -> None:
    """
    Создаёт пользователя, если его раньше не было
    :param session: объект AsyncSession
    :param user_id: айди пользователя
    :param user_name: ну ты понял
    """
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return
    user = User(telegram_id=user_id, user_name=user_name)
    session.add(user)
    await session.commit()


async def get_stations_by_user_id(session: AsyncSession, user_id: int) -> list[UserStations]:
    stmt = select(UserStations.station_name).where(UserStations.telegram_id == user_id)

    res = await session.execute(stmt)
    user_stations = [r[0] for r in res]

    return user_stations


async def ensure_user_station_by_id(session: AsyncSession, user_id: int, station_name: str) -> None:
    user_stations = UserStations(
        telegram_id=user_id,
        station_name=station_name
    )

    session.add(user_stations)

    await session.commit()


async def test_connection(session: AsyncSession) -> int:
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)
