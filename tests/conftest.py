import asyncio
from pathlib import Path

import pytest
import uvloop
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from alembic.command import upgrade, downgrade
from alembic.config import Config as AlembicConfig
from fluentogram import TranslatorHub, TranslatorRunner
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import parse_config, Config
from bot.handlers import get_routers
from bot.middlewares import DbSessionMiddleware, TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub
from bot.utils.secrets import Secret
from tests.mocked_aiogram import MockedBot, MockedSession


@pytest.yield_fixture(scope='session')
def event_loop_policy():
    return uvloop.EventLoopPolicy()
    # return asyncio.get_event_loop_policy()


@pytest.fixture(scope="session")
def event_loop(event_loop_policy):
    asyncio.set_event_loop_policy(event_loop_policy)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Фикстура для получения экземпляра фейкового бота
@pytest.fixture(scope="session")
def bot() -> MockedBot:
    bot = MockedBot()
    bot.session = MockedSession()
    return bot


# Фикстура, которая получает объект настроек
@pytest.fixture(scope="session")
def config() -> Config:
    return parse_config()


# Фикстура, которая создаёт объект конфигурации alembic.ini.BAK для применения миграций
@pytest.fixture(scope="session")
def alembic_config(config: Config) -> AlembicConfig:
    project_dir = Path(__file__).parent.parent
    alembic_ini_path = Path.joinpath(project_dir.absolute(), "alembic.ini").as_posix()
    alembic_cfg = AlembicConfig(alembic_ini_path)

    migrations_dir_path = Path.joinpath(project_dir.absolute(), "bot", "database", "migrations").as_posix()
    alembic_cfg.set_main_option("script_location", migrations_dir_path)
    alembic_cfg.set_main_option("sqlalchemy.url", str(config.db_url))
    return alembic_cfg


# Фикстура для получения асинхронного "движка" для работы с СУБД
@pytest.fixture(scope="session")
def engine(config):
    engine = create_async_engine(str(config.db_url))

    # meta = Base.metadata
    # async with engine.begin() as conn:
    #     await conn.run_sync(meta.drop_all)
    #     await conn.run_sync(meta.create_all)

    yield engine
    engine.sync_engine.dispose()


# @pytest.fixture(scope="function")
@pytest.fixture(scope="session")
def i18n(config) -> TranslatorRunner:
    translator_hub = create_translator_hub(config.locales_path)
    i18n = translator_hub.get_translator_by_locale(locale="ru")

    return i18n


@pytest.fixture(scope="session")
def dp(engine, config) -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # async with session_maker() as once_session:
    #     await prepare_database(once_session, config)

    dispatcher.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    translator_hub: TranslatorHub = create_translator_hub(config.locales_path)
    secrets = tuple(map(Secret.from_text, config.stations_list))

    dispatcher.update.middleware(TranslatorRunnerMiddleware())

    dispatcher.include_routers(*get_routers())

    dispatcher["secrets"] = secrets
    dispatcher["_translator_hub"] = translator_hub
    dispatcher["config"] = config

    return dispatcher


# Фикстура, которая в каждом модуле применяет миграции
# А после завершения тестов в модуле откатывает базу к нулевому состоянию (без данных)
@pytest.fixture(scope="function")
def create(engine, alembic_config: AlembicConfig):
    upgrade(alembic_config, "head")
    yield engine
    # yield
    downgrade(alembic_config, "base")