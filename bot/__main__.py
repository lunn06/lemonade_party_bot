import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import parse_config
from bot.database.base import Base
from bot.database.requests import test_connection, prepare_database
from bot.handlers import get_routers
from bot.middlewares.database import DbSessionMiddleware
from bot.middlewares.i18n import TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub
from bot.utils.secrets import Secret


async def main():
    config = parse_config()

    engine = create_async_engine(url=str(config.db_url), echo=True)

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

    translator_hub: TranslatorHub = create_translator_hub()
    secrets = tuple(map(Secret.from_text, config.stations_list))

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.include_routers(*get_routers())

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        config=config,
        secrets=secrets,
        _translator_hub=translator_hub
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
