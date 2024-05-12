import asyncio

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_reader import parse_config
from bot.database.requests import get_top_users
from bot.filters.admin import AdminFilter

config = parse_config()

router = Router()
router.message.filter(AdminFilter(config.admins))


@router.message(Command("panel"))
async def panel_handler(msg: Message) -> None:
    kb = [
        [types.KeyboardButton(text="Топ пользователей")],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await msg.answer("Вот ваша в тотальном епта-формате", reply_markup=keyboard)


# @router.callback_query(F.data == "top_users")
@router.message(F.text == "Топ пользователей")
async def top_users_handler(msg: Message, session: AsyncSession) -> None:

    top_users = await get_top_users(session)
    # await msg.answer("Ты думаешь, я тебе покажу их?")
    # await asyncio.sleep(3)
    # await msg.answer("Нет.")
    top_users_format = [
        f"user_name: {user.user_name}\nочки: {user.points}\nномер билета: {user.lottery}"
        for user in top_users
    ]

    message = "\n".join(top_users_format)

    await msg.answer(message)
