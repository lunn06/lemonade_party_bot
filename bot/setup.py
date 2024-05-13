from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import Config
from bot.database.base import Base
from bot.database.requests import test_connection, prepare_database
from bot.handlers import get_routers
from bot.middlewares import AntiFloodMiddleware, DbSessionMiddleware, TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub
from bot.utils.secrets import Secret


async def setup_bot(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


async def setup_dp(dp: Dispatcher, config: Config) -> None:
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

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.message.middleware(AntiFloodMiddleware(config.flood_awaiting))
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.include_routers(*get_routers())

    dp["config"] = config
    dp["secrets"] = secrets
    dp["_translator_hub"] = translator_hub


async def setup_webhook(bot: Bot, config: Config, logger) -> None:
    # Check and set webhook for Telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logger.error(f"Can't get webhook info - {e}")
            return

    current_webhook_info = await check_webhook()
    if config.debug_mode:
        logger.debug(f"Current bot info: {current_webhook_info}")
    try:
        await bot.set_webhook(
            f"{config.webhook_url}{config.webhook_path}",
            secret_token=config.telegram_secret_token,
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            # max_connections=40 if config.debug else 100,
        )
        if config.debug_mode:
            logger.debug(f"Updated bot info: {await check_webhook()}")
    except Exception as e:
        logger.error(f"Can't set webhook - {e}")
