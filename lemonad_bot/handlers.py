import random

from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from peewee import IntegrityError

from text import TEXT
from sql import DB
from config import (
    ADMINS,
    DB_NAME,
    SECRETS, 
    NON_UNIQUES,
    STATION_LIST,
    STAR_STATIONS,
    UNSTAR_STATIONS_LIST,
    GIFT_POINTS,
    STAR_STATION_POINTS,
    USUAL_STATION_POINTS,
)

from constants import LOTTERY, MAP_IMAGE_ID

router = Router()
db = DB(DB_NAME)
LOTTERY = 1001

class BotState(StatesGroup):
    is_working = State()
    is_not_working = State()

# @router.message(Command("global_start"))
# async def global_start_hander(msg: Message, state: FSMContext):
#     if msg.from_user.id in ADMINS:
#         await state.set_state(BotState.is_not_working)
#         await msg.answer("Поехали")

@router.message(Command("start"))
async def start_handler(msg: Message): 
    global LOTTERY

    kb = [
        [types.KeyboardButton(text="🎯 Куда пойти?")],
        [types.KeyboardButton(text="🍋 Карта")],
        [types.KeyboardButton(text="🤩 Моя статистика")],
        [types.KeyboardButton(text="🔥 Программа мероприятия")],
        [types.KeyboardButton(text="🥰 Розыгрыш")],
        [types.KeyboardButton(text="🆘 Помощь")],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    try:
        # User.insert(uid=msg.from_user.id, lottery=LOTTERY, star=False, super_star=False, points=0).execute()
        await db.insert_user(uid=msg.from_user.id, lottery=LOTTERY, star=False, super_star=False, points=0)
    except IntegrityError as e:
        print(e)
        # user = User.get(User.uid == msg.from_user.id)
        user = await db.get_user(msg.from_user.id)
        # await msg.answer(TEXT["start"](user.lottery), reply_markup=keyboard)
        await msg.answer(TEXT["start"](user['lottery']), reply_markup=keyboard)
        # await msg.answer_photo(MAP_IMAGE_ID)
        # await send_photo(msg, 'static/map.png')
    else:
        LOTTERY += 1 
        await msg.answer(TEXT["start"](LOTTERY-1), reply_markup=keyboard)
        # await msg.answer_photo(MAP_IMAGE_ID)
        await send_photo(msg, 'static/map.png')


@router.message(F.text.contains("🍋 Куда пойти?") | F.text.contains("куда пойти") | F.text.contains("Куда пойти") )
async def wheretogo_handler(msg: Message):
    # user = User.get(User.uid == msg.from_user.id)
    # user = await db.get(msg.from_user.id)
    user_stations = await get_user_stations(msg.from_user.id)

    await msg.answer(TEXT["wheretogo"])

    answer = "Особые точки:\n\n"
    for station in STAR_STATIONS:
        if station not in user_stations:
            answer += f"⭐️ {station} - {TEXT['station'][station]}\n\n"
        else:
            answer += f"✅ {station} - {TEXT['station'][station]}\n\n"

    answer += "\nОбычные точки:\n\n"
    for station in UNSTAR_STATIONS_LIST:
        if station not in user_stations:
            answer += f"👉 {station} - {TEXT['station'][station]}\n\n"
        else:
            answer += f"✅ {station} - {TEXT['station'][station]}\n\n"

    await msg.answer(answer)


@router.message(F.text.contains("🎯 Карта") | F.text.lower().contains("карта"))
async def statistics_handler(msg: Message):
    await msg.answer(TEXT["infocard"])
    await send_photo(msg, 'static/map.png')
    # await msg.answer_photo(MAP_IMAGE_ID)


@router.message(F.text.contains("🤩 Моя статистика") | F.text.lower().contains("cтатистика"))
async def statistics_handler(msg: Message):
    try:
        # user = User.get(User.uid == msg.from_user.id)
        user = await db.get_user(msg.from_user.id)
        await msg.answer(f"Твои очки: {user['points']}. Номер лотерейного билета: {user['lottery']}")
    except IntegrityError:
        # user = User.create(uid=msg.from_user.id, lottery=LOTTERY, star=False, super_star=False, points=0)
        await msg.answer("Твои очки: 0. Номер лотерейного билета: " + str(1300 + int(random.random() * 100)))


@router.message(F.text.contains("🥰 Розыгрыш"))
async def statistics_handler(msg: Message):
    # user = User.get(User.uid == msg.from_user.id)
    user = await db.get_user(msg.from_user.id)

    await msg.answer(TEXT['lottery'](user['points'], user['lottery']))


@router.message(F.text.contains("🔥 Программа мероприятия") | F.text.lower().contains("программа мероприятия"))
async def statistics_handler(msg: Message):
    await msg.answer(TEXT['programma'])


@router.message(F.text.contains("🆘 Помощь") | F.text.lower().contains("помоги") | F.text.lower().contains("помощь"))
async def statistics_handler(msg: Message):
    await msg.answer(TEXT['help'])

    
# @router.message(F.text.in_(NON_UNIQUES))
# async def nonunique_handler(msg: Message):
#     user = User.get(User.uid == msg.from_user.id)
#     user_codes = get_user_codes(user.uid)
#
#     if msg.text not in user_codes:
#         UserCode.insert(uid=user.uid, code=msg.text, station="gift").execute()
#
#         user.points += GIFT_POINTS
#         user.save()
#
#         await msg.answer(f"Ты нашёл посхалку! {user.points}")
#     else:
#         await msg.answer("Эту посхалку ты уже сканировал!!!!")


@router.message(F.text.regexp(r"^\d{6}$") | F.text.regexp(r"^\d{3} \d{3}$"))
async def unique_handler(msg: Message):
    msg_text = msg.text.replace(' ', '') 

    # user = User.get(User.uid == msg.from_user.id)
    user_stations = await get_user_stations(msg.from_user.id)
    
    # print(user.uid, user_stations)
    for secret in SECRETS:
        if not secret.verify(msg_text):
            continue
        if secret.name in user_stations:
            await msg.answer(f"Верный код! Но ты уже проходил... {secret.name}")
        else:
            # UserCode.insert(uid=user.id, code=msg_text, station=secret.name).execute()
            await db.insert_data(uid=msg.from_user.id, code=msg_text, station=secret.name)
            # user = User.get(User.uid == msg.from_user.id)
            user = await db.get_user(msg.from_user.id)
            user_stations = await get_user_stations(msg.from_user.id)
            # user_stations.append(secret.name)

            if secret.name in STAR_STATIONS:
                # user.points += STAR_STATION_POINTS
                # user.save()
                new_points = user['points'] + STAR_STATION_POINTS
                await db.change_points(user['uid'], new_points)

                answer = f"Ты посетил одну из особых точек: {secret.name}🔥Ты получил {STAR_STATION_POINTS} балла. Итого у тебя их: {new_points}"
            elif secret.name in UNSTAR_STATIONS_LIST:
                # user.points += USUAL_STATION_POINTS
                # user.save()
                new_points = user['points'] + USUAL_STATION_POINTS
                await db.change_points(user['uid'], new_points)

                answer = f"Ты посетил {secret.name}✨ Ты получил {USUAL_STATION_POINTS} балл. Итого у тебя их: {new_points}"
                
            answer += '!'

            if set(STAR_STATIONS).issubset(set(user_stations)) \
                    and not user.star:
                answer = TEXT['star']
                # user.star = True
                # user.save()

                db.change_star(user['uid'], True)

            if sorted(STATION_LIST) == sorted(user_stations) \
                    and not user.super_star:
                answer = TEXT['super_star']
                # user.super_star = True
                # user.save()
                db.change_super_star(user['uid'], True)

            await msg.answer(answer)
        break
    else:
        await msg.answer("Это неверный неверный код 🧐 Уточни его у организатора точки")


@router.message(Command("top"))
async def top_handler(msg: Message, command: CommandObject):
    if msg.from_user.id in ADMINS:
        try:
            limit = int(command.args)
        except TypeError:
            await msg.answer("Укажи количество: /top <количество>")
        else:
            with db.atomic():
                ordered_users = User.select().order_by(User.points)

                top = [f"{user.lottery} -> {user.points}\n" for user in ordered_users][:limit]

            await msg.answer(' '.join(map(str, top)))

@router.message(Command("get_all"))
async def get_all_handler(msg: Message):
    if msg.from_user.id in ADMINS:
        lotteries = User.select()
        lotteries = map(lambda user: user.lottery, lotteries)
        answer = ""
        for l in lotteries:
            answer += f"{l}\n"

        await msg.answer(answer)


@router.message()
async def unexpected_handler(msg: Message):
    await msg.answer(TEXT['unexpected'])

async def send_photo(msg: Message, photo: str):
    file = FSInputFile(photo)
    send_file_object = await msg.answer_photo(photo=file)
    print(send_file_object.photo[0].file_id)

    # await msg.answer_photo(MAP_IMAGE_ID)

async def get_user_stations(uid: str):
    # with db.atomic():
    #     user = User.get(User.uid == uid)
    #     user_stations = UserCode.select().where(user.uid == uid)

    data_list = await db.get_data(uid)

    # return list(map(lambda user: user.station, user_stations))
    return list(map(lambda data: data['station'], data_list))

async def get_user_codes(uid: str):
    # with db.atomic():
    #     user = User.get(User.uid == uid)
    #     user_codes = UserCode.select().where(user.uid == uid)
    #
    # return list(map(lambda user: user.code, user_codes))

    data_list = await db.get_data(uid)
    return list(map(lambda data: data['code'], data_list))

