import random
from collections import deque
from datetime import datetime
from typing import TYPE_CHECKING

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, Message, User
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from bot.config_reader import Config, parse_config
from bot.database.requests import ensure_user, ensure_user_station_by_id
from tests.mocked_aiogram import MockedBot

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

config = parse_config()


def make_incoming_message(user_id: int, text: str, msg_id: int = 1) -> Message:
    chat = Chat(id=user_id, type=ChatType.PRIVATE)
    return Message(
        message_id=msg_id,
        chat=chat,
        from_user=User(id=chat.id, is_bot=False, first_name="test", username="test", language_code="ru"),
        date=datetime.now(),
        text="🎯 Куда пойти?",
    )


users = [i for i in range(1, 9999999)]
random.shuffle(users)
user_queue = deque(users)


def random_user_id() -> int:
    return user_queue.pop()


def wheretogo_message(user_stations: list[str], i18n: TranslatorRunner, config: Config) -> str:
    answer = i18n.station.header(type="star")
    answer += "\n\n"
    for station in config.star_stations:
        station_name = i18n.station.name(station=station)
        station_description = i18n.station.description(station=station)
        if station not in user_stations:
            answer += i18n.undone.station(
                type="star",
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"
        else:
            answer += i18n.done.station(
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"

    answer += i18n.station.header(type="unstar")
    answer += "\n\n"
    unstar_stations = [st for st in config.stations_list if st not in config.star_stations]
    for station in unstar_stations:
        station_name = i18n.station.name(station=station)
        station_description = i18n.station.description(station=station)
        if station not in user_stations:
            answer += i18n.undone.station(
                type="unstar",
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"
        else:
            answer += i18n.done.station(
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"
    return answer


@pytest.mark.parametrize(
    "user_stations",
    [config.stations_list[:i] for i in range(0, len(config.stations_list) + 1)]
)
def test_wheretogo_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        config: Config,
        create: AsyncEngine,
        user_stations: list[str],
        event_loop
):
    event_loop.run_until_complete(_test_wheretogo_message(dp, bot, i18n, config, create, user_stations))


async def _test_wheretogo_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        config: Config,
        create: AsyncEngine,
        user_stations: list[str]
):
    async with AsyncSession(create) as session:
        user_id = random_user_id()
        await ensure_user(session, user_id=user_id, user_name="test")

        for station in user_stations:
            await ensure_user_station_by_id(session, user_id, station)

        bot.add_result_for(
            ok=True,
            method=SendMessage
        )

        bot.add_result_for(
            ok=True,
            method=SendMessage
        )

        incomming_message = make_incoming_message(user_id, i18n.wheretogo.button())
        update = await dp.feed_update(
            bot,
            Update(message=incomming_message, update_id=1)
        )

        awaiting_message = wheretogo_message(user_stations, i18n, config)
        assert update is not UNHANDLED
        outgoing_message: TelegramType = bot.get_request()
        print(outgoing_message.text)
        assert outgoing_message.text == awaiting_message
