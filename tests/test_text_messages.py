import random
from datetime import datetime
from typing import TYPE_CHECKING

from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Chat, Message, User, Update
from fluentogram import TranslatorRunner
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from bot.database.models import User as DbUser
from bot.database.requests import ensure_user, get_user_by_id
from tests.mocked_aiogram import MockedBot

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


def make_incoming_message(user_id: int, text: str, msg_id: int = 1) -> Message:
    chat = Chat(id=user_id, type=ChatType.PRIVATE)
    return Message(
        message_id=msg_id,
        chat=chat,
        from_user=User(id=chat.id, is_bot=False, first_name="test", username="test", language_code="ru"),
        date=datetime.now(),
        text=text,
    )


def random_user_id() -> int:
    return random.randint(10000, 99999)


def test_start_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
        event_loop
) -> None:
    event_loop.run_until_complete(_test_start_message(dp, bot, i18n, create))


async def _test_start_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
) -> None:
    async with AsyncSession(create) as session:
        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )
        user_id = random_user_id()

        incoming_message = make_incoming_message(user_id, "/start")
        update = await dp.feed_update(
            bot,
            Update(message=incoming_message, update_id=1)
        )

        stmt = select(DbUser).where(DbUser.telegram_id == user_id)
        user_response = await session.scalar(stmt)

        awaited_start_message = i18n.start.message(lottery=user_response.lottery)
        assert update is not UNHANDLED
        outgoing_message: TelegramType = bot.get_request()
        assert isinstance(outgoing_message, SendMessage)
        assert outgoing_message.text == awaited_start_message


def test_lottery_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
        event_loop
) -> None:
    event_loop.run_until_complete(_test_lottery_message(dp, bot, i18n, create))


async def _test_lottery_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
) -> None:
    async with AsyncSession(create) as session:
        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )
        user_id = random_user_id()
        await ensure_user(session, user_id, user_name="test")

        incoming_message = make_incoming_message(user_id, i18n.lottery.button())
        update = await dp.feed_update(
            bot,
            Update(message=incoming_message, update_id=1)
        )

        user_response = await get_user_by_id(session, user_id)

        awaited_lottery_message = i18n.lottery.message(
            lottery=user_response.lottery,
            points=user_response.points
        )
        assert update is not UNHANDLED
        outgoing_message: TelegramType = bot.get_request()
        assert isinstance(outgoing_message, SendMessage)
        assert outgoing_message.text == awaited_lottery_message


def test_schedule_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        event_loop
) -> None:
    event_loop.run_until_complete(_test_schedule_message(dp, bot, i18n))


async def _test_schedule_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
) -> None:
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    user_id = random_user_id()

    incoming_message = make_incoming_message(user_id, i18n.programma.button())
    update = await dp.feed_update(
        bot,
        Update(message=incoming_message, update_id=1)
    )

    awaited_schedule_message = i18n.programma.message()
    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == awaited_schedule_message


def test_help_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        event_loop
) -> None:
    event_loop.run_until_complete(_test_help_message(dp, bot, i18n))


async def _test_help_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
) -> None:
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    user_id = random_user_id()

    incoming_message = make_incoming_message(user_id, i18n.help.button())
    update = await dp.feed_update(
        bot,
        Update(message=incoming_message, update_id=1)
    )

    awaited_help_message = i18n.help.message()
    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == awaited_help_message


def test_infocard_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
        event_loop
) -> None:
    event_loop.run_until_complete(_test_infocard_message(dp, bot, i18n, create))


async def _test_infocard_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
) -> None:
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас не нужен
    )

    user_id = random_user_id()

    update = await dp.feed_update(
        bot,
        Update(
            message=make_incoming_message(user_id, i18n.infocard.button(), msg_id=3),
            update_id=2
        )
    )

    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == i18n.infocard.message()


def test_statistics_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create,
        event_loop,
) -> None:
    event_loop.run_until_complete(_test_statistics_message(dp, bot, i18n, create, True))
    event_loop.run_until_complete(_test_statistics_message(dp, bot, i18n, create, False))


async def _test_statistics_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        create: AsyncEngine,
        authorized: bool,
) -> None:
    async with AsyncSession(create) as session:
        user_id = random_user_id()
        if authorized:
            await ensure_user(session=session, user_id=user_id, user_name='test')

        bot.add_result_for(
            method=SendMessage,
            ok=True,
        )

        statistics_button_text = i18n.statistics.button()
        update = await dp.feed_update(
            bot,
            Update(message=make_incoming_message(user_id, statistics_button_text), update_id=3 if authorized else 4)
        )

        user_response = await get_user_by_id(session=session, user_id=user_id)

        assert update is not UNHANDLED
        outgoing_message: TelegramType = bot.get_request()
        assert isinstance(outgoing_message, SendMessage)
        if authorized:
            assert outgoing_message.text == i18n.statistics.message(
                points=user_response.points, lottery=user_response.lottery
            )
        else:
            assert outgoing_message.text == i18n.start.command.request()
