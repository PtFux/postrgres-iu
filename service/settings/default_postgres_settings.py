import asyncio

from secret_env import SecretEnv
from service.repositories.base.declarative_base import DeclarativeBase
from service.settings.postgres_settings import PostgresSettings


DEFAULT_POSTGRES_SETTINGS = PostgresSettings(
        db_name=SecretEnv.db_name,
        username=SecretEnv.username,
        password=SecretEnv.password,
        port=SecretEnv.port,
        host=SecretEnv.host,
        declarative_base=DeclarativeBase
    )