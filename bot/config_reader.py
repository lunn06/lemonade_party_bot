from environs import Env
from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

env = Env()
env.read_env()


class Config(BaseSettings):
    bot_token: SecretStr

    debug_mode: bool
    db_url: PostgresDsn
    admins: list[int]
    stations_list: list[str]
    star_stations: list[str]
    star_station_points: int
    usual_station_points: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def parse_config() -> Config:
    return Config()


if __name__ == "__main__":
    config = parse_config()
    print(config.model_dump())
