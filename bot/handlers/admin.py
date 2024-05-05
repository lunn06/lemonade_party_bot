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
async def panel_handler(msg: Message):
    kb = [
        [types.KeyboardButton(text="Топ пользователей")],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await msg.answer("Вот ваша в тотальном епта-формате", reply_markup=keyboard)


# @router.callback_query(F.data == "top_users")
@router.message(F.text == "Топ пользователей")
async def top_callback(msg: Message, session: AsyncSession):

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


@router.message(Command("get_all"))
async def get_all_handler(msg: Message):
    if msg.from_user.id in ADMINS:
        lotteries = User.select()
        lotteries = map(lambda user: user.lottery, lotteries)
        answer = ""
        for l in lotteries:
            answer += f"{l}\n"

        await msg.answer(answer)


async def send_photo(msg: Message, photo: str):
    file = FSInputFile(photo)
    send_file_object = await msg.answer_photo(photo=file)
    print(send_file_object.photo[0].file_id)

    # await msg.answer_photo(MAP_IMAGE_ID)


# async def get_user_stations(uid: str):
#     # with db.atomic():
#     #     user = User.get(User.uid == uid)
#     #     user_stations = UserCode.select().where(user.uid == uid)
#
#     data_list = await get_stations_by_user_id()
#
#     # return list(map(lambda user: user.station, user_stations))
#     return list(map(lambda data: data['station'], data_list))


async def get_user_codes(uid: str):
    # with db.atomic():
    #     user = User.get(User.uid == uid)
    #     user_codes = UserCode.select().where(user.uid == uid)
    #
    # return list(map(lambda user: user.code, user_codes))

    data_list = await db.get_data(uid)
    return list(map(lambda data: data['code'], data_list))
