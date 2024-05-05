from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Chat, Message, User, Update
from fluentogram import TranslatorRunner
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User as DbUser
from tests.mocked_aiogram import MockedBot


def make_incoming_message(chat: Chat) -> Message:
    return Message(
        message_id=1,
        chat=chat,
        from_user=User(id=chat.id, is_bot=False, first_name="User"),
        date=datetime.now(),
        text="/start"
    )


@pytest.mark.asyncio
async def test_start_message(dp: Dispatcher, bot: MockedBot, i18n: TranslatorRunner, session: AsyncSession):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас не нужен
    )

    user_id = 123456
    chat = Chat(id=user_id, type=ChatType.PRIVATE)

    await dp.feed_update(
        bot,
        Update(message=make_incoming_message(chat), update_id=1)
    )

    stmt = select(DbUser).where(DbUser.telegram_id == user_id).limit(1)
    user_response = await session.scalar(stmt)

    # assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == i18n.start.message(lottery=user_response.lottery)
