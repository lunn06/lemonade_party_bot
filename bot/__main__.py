import logging
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Annotated

import uvicorn
import uvloop
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from fastapi import FastAPI, Header
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette.requests import Request

from bot.config_reader import parse_config
from bot.database.base import Base
from bot.database.requests import test_connection, prepare_database
from bot.handlers import get_routers
from bot.middlewares.database import DbSessionMiddleware
from bot.middlewares.i18n import TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub
from bot.utils.secrets import Secret
from bot.webhook import set_webhook


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AbstractAsyncContextManager[None]:
    await setup_dp(dp)
    await setup_bot(bot)
    await set_webhook(bot, config, logger)
    yield


config = parse_config()
logger = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan)
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)


@app.post(config.webhook_path)
async def webhook(
        request: Request,
        x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None
) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != config.telegram_secret_token:
        logger.error("Wrong secret token !")
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = Update(**(await request.json()))
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


async def setup_bot(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


async def setup_dp(dp: Dispatcher) -> None:
    engine = create_async_engine(url=str(config.db_url), echo=config.debug_mode)

    if config.empty_db:
        meta = Base.metadata
        async with engine.begin() as conn:
            if config.debug_mode:
                await conn.run_sync(meta.drop_all)
            await conn.run_sync(meta.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=config.debug_mode)

    async with session_maker() as session:
        await test_connection(session)
        if config.debug_mode:
            await prepare_database(session, config)

    translator_hub: TranslatorHub = create_translator_hub(config.locales_path)
    secrets = tuple(map(Secret.from_text, config.stations_list))

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.include_routers(*get_routers())

    dp["config"] = config
    dp["secrets"] = secrets
    dp["_translator_hub"] = translator_hub


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if config.debug_mode:
        async def run_bot():
            await dp.start_polling(bot)
        uvloop.run(run_bot())
    else:
        uvicorn.run(app, port=config.port, loop="uvloop")
