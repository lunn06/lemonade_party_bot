import sqlalchemy.exc
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_reader import Config
from bot.database.requests import (
    ensure_user,
    get_user_by_id,
    get_stations_by_user_id,
    ensure_user_station_by_id
)
from bot.utils.i18n import create_translator_hub
from bot.utils.secrets import Secret
from bot.utils.telegram import build_keyboard

router = Router()
outer_translator_hub = create_translator_hub()
outer_i18n_ru = outer_translator_hub.get_translator_by_locale("ru")


class BotState(StatesGroup):
    is_working = State()
    is_not_working = State()


@router.message(CommandStart())
async def start_handler(msg: Message, session: AsyncSession, i18n: TranslatorRunner):
    keyboard = build_keyboard(
        i18n.wheretogo.button(),
        i18n.infocard.button(),
        i18n.statistics.button(),
        i18n.programma.button(),
        i18n.lottery.button(),
        i18n.help.button(),
    )

    try:
        await ensure_user(session, user_id=msg.from_user.id, user_name=msg.from_user.full_name)
    except sqlalchemy.exc.IntegrityError:
        await ensure_user(session, user_id=msg.from_user.id, user_name=msg.from_user.full_name)

    user = await get_user_by_id(session, msg.from_user.id)
    # user = await get_user_by_id(session, msg.from_user.id)

    start_message = i18n.start.message(lottery=user.lottery)
    await msg.answer(start_message, reply_markup=keyboard)
    # await send_photo(msg, 'static/map.png')


# @router.message(F.text.contains("🍋 Куда пойти?") | F.text.contains("куда пойти") | F.text.contains("Куда пойти"))
@router.message(F.text.contains(outer_i18n_ru.wheretogo.button()))
async def wheretogo_handler(msg: Message, session: AsyncSession, i18n: TranslatorRunner, config: Config):
    user_stations = await get_stations_by_user_id(session, msg.from_user.id)
    # user_stations = [u.station_name for u in user_stations_rows]

    await msg.answer(i18n.wheretogo.message())

    answer = i18n.station.header(type="star")
    answer += "\n\n"
    for station in config.star_stations:
        station_name = i18n.station.name(station=station)
        station_description = i18n.station.description(station=station)
        if station not in user_stations:
            answer += i18n.undone.station(
                type="star",
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"
        else:
            answer += i18n.done.station(
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"

    answer += i18n.station.header(type="unstar")
    answer += "\n\n"
    unstar_stations = [st for st in config.stations_list if st not in config.star_stations]
    for station in unstar_stations:
        station_name = i18n.station.name(station=station)
        station_description = i18n.station.description(station=station)
        if station not in user_stations:
            # answer += f"👉 {station} - {TEXT['station'][station]}\n\n"
            answer += i18n.undone.station(
                type="unstar",
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"
        else:
            answer += i18n.done.station(
                station_name=station_name,
                description=station_description
            )
            answer += "\n\n"

    await msg.answer(answer)


# @router.message(F.text.contains("🎯 Карта") | F.text.lower().contains("карта"))
@router.message(F.text.contains(outer_i18n_ru.infocard.button()))
async def infocard_handler(msg: Message, i18n: TranslatorRunner):
    await msg.answer(i18n.infocard.message())
    # await send_photo(msg, 'static/map.png')
    # await msg.answer_photo(MAP_IMAGE_ID)


# @router.message(F.text.contains("🤩 Моя статистика") | F.text.lower().contains("cтатистика"))
@router.message(F.text.contains(outer_i18n_ru.statistics.button()))
async def statistics_handler(msg: Message, session: AsyncSession, i18n: TranslatorRunner):
    user = await get_user_by_id(session, msg.from_user.id)
    if user is None:
        await msg.answer(i18n.start.command.request())
    else:
        await msg.answer(i18n.statistics.message(points=user.points, lottery=user.lottery))


# @router.message(F.text.contains("🥰 Розыгрыш"))
@router.message(F.text.contains(outer_i18n_ru.lottery.button()))
async def lottery_handler(msg: Message, session: AsyncSession, i18n: TranslatorRunner):
    user = await get_user_by_id(session, msg.from_user.id)
    if user is None:
        await msg.answer(i18n.start.command.request())
    else:
        await msg.answer(i18n.lottery.message(points=user.points, lottery=user.lottery))


# @router.message(F.text.contains("🔥 Программа мероприятия") | F.text.lower().contains("программа мероприятия"))
@router.message(F.text.contains(outer_i18n_ru.programma.button()))
async def schedule_handler(msg: Message, i18n: TranslatorRunner):
    await msg.answer(i18n.programma.message())


# @router.message(F.text.contains("🆘 Помощь") | F.text.lower().contains("помоги") | F.text.lower().contains("помощь"))
@router.message(Command("help"))
@router.message(F.text.contains(outer_i18n_ru.help.button()))
async def help_handler(msg: Message, i18n: TranslatorRunner):
    await msg.answer(i18n.help.message())


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
async def unique_handler(
        msg: Message,
        session: AsyncSession,
        config: Config,
        i18n: TranslatorRunner,
        secrets: list[Secret]
):
    msg_text = msg.text.replace(' ', '')

    user_stations_names = await get_stations_by_user_id(session, msg.from_user.id)
    # user_stations_names = list(st.station_name for st in user_stations)

    for secret in secrets:
        if not secret.verify(msg_text):
            continue

        station = secret.name
        station_name = i18n.station.name(station=station)
        if station in user_stations_names:
            await msg.answer(i18n.doubled.station(station_name=station_name))
            return

        await ensure_user_station_by_id(session, msg.from_user.id, station)

        user = await get_user_by_id(session, msg.from_user.id)
        if station in config.star_stations:
            user.points += config.star_station_points
            answer = i18n.station.arrangement(
                type="star",
                station_name=station_name,
                station_points=config.star_station_points,
                user_points=user.points
            )
        else:
            user.points += config.usual_station_points
            answer = i18n.station.arrangement(
                type="unstar",
                station_name=station_name,
                station_points=config.usual_station_points,
                user_points=user.points
            )
        await session.commit()

        user_stations_names += [secret.name]

        if set(config.star_stations).issubset(set(user_stations_names)):
            answer = i18n.star.message()

        if sorted(config.stations_list) == sorted(user_stations_names):
            answer = i18n.superstar.message()

        await msg.answer(answer)
        return

    await msg.answer(i18n.wrong.code.message())


@router.message()
async def unexpected_handler(msg: Message, i18n: TranslatorRunner):
    await msg.answer(i18n.unexpected.message())
