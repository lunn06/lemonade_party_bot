from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, F
from aiogram.dispatcher.flags import get_flag, check_flags
from aiogram.types import TelegramObject, Message, CallbackQuery, User
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import ensure_user, get_user_by_id


class EnsureUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        session: AsyncSession = data.get("session")

        # user_request_flag = get_flag(data, "user_request")
        # user_request_flag = check_flags(data, F.contains())
        ensured = False
        dbuser = await ensure_user(session, user_id=user.id, user_name=user.username)
        if dbuser is None:
            ensured = True
            dbuser = await get_user_by_id(session, user_id=user.id)
        data["user"] = dbuser
        data["user_ensured"] = ensured

        await handler(event, data)
