from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from fluentogram import TranslatorRunner

from bot.config_reader import parse_config
from bot.database.requests import get_top_users
from bot.filters.admin import AdminFilter
# from bot.locales.stub import TranslatorRunner

config = parse_config()

router = Router()
router.message.filter(AdminFilter(config.admins))


@router.message(Command("lottery"))
async def lottery_handler(msg: Message, session: AsyncSession, i18n: TranslatorRunner) -> None:
    top_users = await get_top_users(session)

    answer = ""
    for user in top_users:
        answer += i18n.top.user.template(
            user_name=user.user_name,
            points=user.points,
            lottery=user.lottery,
            quest_time=str(user.quest_time)
        )
        answer += "\n\n"

    await msg.answer(answer)

    # await msg.answer()
