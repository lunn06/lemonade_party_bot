import uvloop
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from bot.config_reader import parse_config, Config
from bot.database.models import User
from bot.filters.admin import AdminFilter
from bot.middlewares import DbSessionMiddleware

config: Config = parse_config()
bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.update.filter(AdminFilter(config.admins))

class SendState(StatesGroup):
    confirmed = State()
    sended = State()

async def main():
    engine = create_async_engine(url=str(config.db_url), echo=config.debug_mode)

    session_maker = async_sessionmaker(engine, expire_on_commit=config.debug_mode)

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    await dp.start_polling(bot)


@dp.message()
async def send_message_handler(msg: Message, session: AsyncSession, bot: Bot):
    user_stmnt = select(User.telegram_id)
    users = await session.execute(user_stmnt)

    for user_id in users:
        user_id = user_id[0]
        print(user_id)
        await bot.send_message(chat_id=user_id, text=msg.text)

if __name__ == '__main__':
    uvloop.run(main())