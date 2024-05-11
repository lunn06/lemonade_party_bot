# exist
#   done
#       star
#       star_user
#       unstar
#       super_star_user
#   undone
# not exist
import datetime
import random
from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update
from fluentogram import TranslatorRunner
from pyotp import TOTP
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.config_reader import Config
from bot.database.requests import ensure_user, ensure_user_station_by_id
from tests.mocked_aiogram import MockedBot
from tests.test_text_messages import make_incoming_message

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


def random_user_id():
    return random.randint(1, 999999)


def test_not_existing_unique(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        event_loop: AbstractEventLoop
) -> None:
    event_loop.run_until_complete(
        _test_not_existing_unique(
            dp, bot, i18n, create
        )
    )


async def _test_not_existing_unique(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
) -> None:
    async with AsyncSession(create) as session:
        user_id = random_user_id()
        await ensure_user(session=session, user_id=user_id, user_name='test')

        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )

        update = await dp.feed_update(
            bot,
            Update(
                message=make_incoming_message(user_id, "000 000"),
                update_id=1
            )
        )

        awaiting_message = i18n.wrong.code.message()
        assert update is not UNHANDLED

        outgoing_message: TelegramType = bot.get_request()
        assert outgoing_message.text == awaiting_message


def test_done_unique(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        event_loop: AbstractEventLoop
) -> None:
    event_loop.run_until_complete(
        _test_done_unique(
            dp, bot, i18n, create
        )
    )


async def _test_done_unique(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
) -> None:
    async with AsyncSession(create) as session:
        user_id = random_user_id()
        await ensure_user(session=session, user_id=user_id, user_name='test')

        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )

        checking_secret = random.choice(dp["secrets"])
        await ensure_user_station_by_id(session, user_id, checking_secret.name)

        checking_totp: TOTP = checking_secret.secret
        now = datetime.datetime.now()
        true_code = checking_totp.at(now)

        update = await dp.feed_update(
            bot,
            Update(
                message=make_incoming_message(user_id, str(true_code)),
                update_id=1
            )
        )

        station_name = i18n.station.name(station=checking_secret.name)
        awaiting_message = i18n.doubled.station(station_name=station_name)
        assert update is not UNHANDLED

        outgoing_message: TelegramType = bot.get_request()
        assert outgoing_message.text == awaiting_message


@pytest.mark.parametrize(
    "station_type",
    [
        "star", "unstar"
    ]
)
def test_unique(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        event_loop: AbstractEventLoop,
        config: Config,
        station_type: str
) -> None:
    event_loop.run_until_complete(
        _test_unique(
            dp, bot, i18n, create, config, station_type
        )
    )


async def _test_unique(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        config: Config,
        station_type: str,
) -> None:
    async with AsyncSession(create) as session:
        user_id = random_user_id()
        await ensure_user(session=session, user_id=user_id, user_name='test')

        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )

        if station_type == "star":
            checking_secret = random.choice([sec for sec in dp["secrets"] if sec.name in config.star_stations])
        else:
            # unstar_stations = [st for st in config.stations_list if st not in config.star_stations]
            # checking_secret = random.choice(unstar_stations)
            checking_secret = random.choice([sec for sec in dp["secrets"] if sec.name not in config.star_stations])

        checking_totp: TOTP = checking_secret.secret
        now = datetime.datetime.now()
        true_code = checking_totp.at(now)
        station_points = config.star_station_points if station_type == "star" else config.usual_station_points

        update = await dp.feed_update(
            bot,
            Update(
                message=make_incoming_message(user_id, str(true_code)),
                update_id=1
            )
        )

        station_name = i18n.station.name(station=checking_secret.name)
        awaiting_message = i18n.station.arrangement(
            type=station_type,
            station_name=station_name,
            station_points=station_points,
            user_points=station_points
        )
        assert update is not UNHANDLED

        outgoing_message: TelegramType = bot.get_request()
        assert outgoing_message.text == awaiting_message


@pytest.mark.parametrize(
    "message_type",
    [
        "star", "super_star"
    ]
)
def test_star_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        event_loop: AbstractEventLoop,
        config: Config,
        message_type: str
) -> None:
    event_loop.run_until_complete(
        _test_star_message(
            dp, bot, i18n, create, config, message_type
        )
    )


async def _test_star_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        config: Config,
        message_type: str,
) -> None:
    async with (AsyncSession(create) as session):
        user_id = random_user_id()
        await ensure_user(session=session, user_id=user_id, user_name='test')

        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )

        if message_type == "star":
            inserting, checking = config.star_stations[:-1], config.star_stations[-1]
        else:
            inserting, checking = config.stations_list[:-1], config.stations_list[-1]
        for st in inserting:
            await ensure_user_station_by_id(session, user_id, st)

        checking_secret = [sec for sec in dp["secrets"] if sec.name == checking][0]

        checking_totp: TOTP = checking_secret.secret
        now = datetime.datetime.now()
        true_code = checking_totp.at(now)

        # if checking in config.star_stations:
        #     station_points = config.star_station_points
        #     station_type = "star"
        # else:
        #     station_type = "unstar"
        #     station_points = config.usual_station_points

        update = await dp.feed_update(
            bot,
            Update(
                message=make_incoming_message(user_id, str(true_code)),
                update_id=1
            )
        )

        if message_type == "star":
            awaiting_message = i18n.star.message()
        else:
            awaiting_message = i18n.superstar.message()
        # station_name = i18n.station.name(station=checking_secret.name)
        # awaiting_message = i18n.station.arrangement(
        #     type=station_type,
        #     station_name=station_name,
        #     station_points=station_points,
        #     user_points=station_points
        # )
        assert update is not UNHANDLED

        outgoing_message: TelegramType = bot.get_request()
        assert outgoing_message.text == awaiting_message
