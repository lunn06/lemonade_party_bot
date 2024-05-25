
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config_reader import parse_config
from bot.filters.admin import AdminFilter

config = parse_config()

router = Router()
router.message.filter(AdminFilter(config.admins))


@router.message(Command("lottery"))
async def panel_handler(msg: Message) -> None:
    ...
