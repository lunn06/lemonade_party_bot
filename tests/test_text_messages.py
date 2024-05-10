import random
from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Chat, Message, User, Update
from fluentogram import TranslatorRunner
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User as DbUser
from bot.database.requests import ensure_user, get_user_by_id
from tests.mocked_aiogram import MockedBot


def make_incoming_message(chat: Chat, text: str, msg_id: int = 1) -> Message:
    return Message(
        message_id=msg_id,
        chat=chat,
        from_user=User(id=chat.id, is_bot=False, first_name="User"),
        date=datetime.now(),
        text=text
    )


def random_user_id() -> int:
    return random.randint(10000, 99999)


# def _test_start_message(
#         dp: Dispatcher,
#         bot: MockedBot,
#         i18n: TranslatorRunner,
#         session,
#         # event_loop: AbstractEventLoop,
# ):
#     # event_loop = asyncio.new_event_loop()
#     # event_loop.run_until_complete(_test_start_message(dp, bot, i18n, session))
#     ...


# @pytest.mark.asyncio
async def test_start_message(dp: Dispatcher, bot: MockedBot, i18n: TranslatorRunner, session: AsyncSession) -> None:
    # async with AsyncSession(engine) as session:
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас не нужен
    )
    user_id = random_user_id()
    chat = Chat(id=user_id, type=ChatType.PRIVATE)

    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(chat, "/start"), update_id=1)
    )

    stmt = select(DbUser).where(DbUser.telegram_id == user_id).limit(1)
    user_response = await session.scalar(stmt)

    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == i18n.start.message(lottery=user_response.lottery)


# @pytest.mark.asyncio
# def _test_infocard_message(dp: Dispatcher, bot: MockedBot, i18n: TranslatorRunner, event_loop: AbstractEventLoop):
#     # event_loop = asyncio.new_event_loop()
#     event_loop.run_until_complete(_test_infocard_message(dp, bot, i18n))


# @pytest.mark.asyncio
async def test_infocard_message(dp: Dispatcher, bot: MockedBot, i18n: TranslatorRunner):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас не нужен
    )

    user_id = random_user_id()
    chat = Chat(id=user_id, type=ChatType.PRIVATE)

    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(
            chat, i18n.infocard.button(), msg_id=3),
            update_id=2)
    )

    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == i18n.infocard.message()


# def _test_statistics_message(
#         dp: Dispatcher,
#         bot: MockedBot,
#         i18n: TranslatorRunner,
#         session: AsyncSession,
#         # event_loop: AbstractEventLoop,
# ):
#     # event_loop.run_until_complete(_test_statistics_message(dp, bot, i18n, session, True))
#     # event_loop.run_until_complete(_test_statistics_message(dp, bot, i18n, session, False))
#     ...


@pytest.mark.parametrize(
    "authorized",
    [
        True,
        False,
    ]
)
async def test_statistics_message(
        dp: Dispatcher,
        bot: MockedBot,
        i18n: TranslatorRunner,
        session: AsyncSession,
        authorized: bool
):
    # async with AsyncSession(engine) as session:
    user_id = random_user_id()
    if authorized:
        await ensure_user(session=session, user_id=user_id, user_name='test')

    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )

    chat = Chat(id=user_id, type=ChatType.PRIVATE)

    statistics_button_text = i18n.statistics.button()
    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(chat, statistics_button_text), update_id=3 if authorized else 4)
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
