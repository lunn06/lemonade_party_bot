from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_reader import parse_config
from bot.database.requests import get_top_users
from bot.filters.admin import AdminFilter

config = parse_config()

router = Router()
router.message.filter(AdminFilter(config.admins))


@router.message(Command("lottery"))
async def lottery_handler(msg: Message, session: AsyncSession) -> None:
    top_users = await get_top_users(session)

    answer = ""
    for user in top_users:
        for _ in range(50):
            answer += f'''\
Имя: {user.user_name}
Очки: {user.points}
Лоттерейный билет: {user.lottery}
Время прохождения точкек: {user.quest_time}\n\n \
'''

    await msg.answer(answer)

    # await msg.answer()
