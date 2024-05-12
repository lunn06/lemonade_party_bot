from aiogram import Bot
from aiogram.types import WebhookInfo

from bot.config_reader import Config


async def set_webhook(bot: Bot, config: Config, logger) -> None:
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
