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
from starlette.requests import Request

from bot.config_reader import parse_config
from bot.setup import setup_dp, setup_bot, setup_webhook

config = parse_config()
logger = logging.getLogger(__name__)
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AbstractAsyncContextManager[None]:
    await setup_dp(dp, config)
    await setup_bot(bot)
    await setup_webhook(bot, config, logger)
    yield


async def webhook(
        request: Update,
        x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None
) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != config.telegram_secret_token:
        logger.error("Wrong secret token !")
        return {"status": "error", "message": "Wrong secret token !"}
    # telegram_update = Update(**(await request.json()))
    await dp.feed_webhook_update(bot=bot, update=request)


def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.post(config.webhook_path)(webhook)

    return app


async def run_bot(dp, bot):
    await setup_dp(dp, config)
    await setup_bot(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if config.debug_mode:
        uvloop.run(run_bot(dp, bot))
    else:
        app = get_app()
        uvicorn.run(app, port=config.port, loop="uvloop", interface="asgi3")
