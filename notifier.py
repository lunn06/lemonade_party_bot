import asyncio

import uvloop
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from fluentogram import TranslatorHub, TranslatorRunner
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from bot.config_reader import parse_config, Config
from bot.database.models import User
from bot.database.requests import get_user_by_id
from bot.filters.admin import AdminFilter
from bot.middlewares import DbSessionMiddleware, TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub

config: Config = parse_config()
bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.delete_webhook()
dp = Dispatcher()


class SendState(StatesGroup):
    confirmed = State()
    sended = State()


async def main():
    engine = create_async_engine(url=str(config.db_url), echo=config.debug_mode)
    session_maker = async_sessionmaker(engine, expire_on_commit=config.debug_mode)

    translator_hub: TranslatorHub = create_translator_hub(config.locales_path)

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.update.middleware(TranslatorRunnerMiddleware())

    dp["_translator_hub"] = translator_hub

    await dp.start_polling(bot)


@dp.message(AdminFilter(config.admins))
async def send_message_handler(msg: Message, session: AsyncSession, bot: Bot):
    user_stmnt = select(User.telegram_id)
    users = await session.execute(user_stmnt)

    for user_id in users:
        user_id = user_id[0]
        await asyncio.sleep(0.04)
        await bot.send_message(chat_id=user_id, text=msg.text)


@dp.message()
async def usual_handler(msg: Message, session: AsyncSession, i18n: TranslatorRunner):
    user = await get_user_by_id(session, msg.from_user.id)
    if user is None:
        await msg.answer("Прости, но часть с интерактивными точками уже закончилась(")
    else:
        await msg.answer("Часть с интерактивными точками уже закончена! Могу показать только твою статистику")
        await msg.answer(i18n.statistics.message(points=user.points, lottery=user.lottery))


if __name__ == '__main__':
    uvloop.run(main())
