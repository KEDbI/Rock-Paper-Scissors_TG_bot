from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tgbot: TgBot


@dataclass
class Database:
    database_name: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class DatabaseConfig:
    db: Database


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tgbot=TgBot(token=env('TOKEN')))


def connect_database(path: str | None = None) -> DatabaseConfig:
    env: Env = Env()
    env.read_env(path)
    return DatabaseConfig(db=Database(
        database_name=env('DATABASE'),
        user=env('USER'),
        password=env('PASSWORD'),
        host=env('HOST'),
        port=env('PORT')
    ))
