import asyncio

from bot_scheduler import BotScheduler
from repositories.base.declarative_base import DeclarativeBase
from repositories.postgres_repository import PostgresRepository
from secret_env import SecretEnv
from service.settings.postgres_settings import PostgresSettings


async def main():
    connection = PostgresSettings(
        db_name=SecretEnv.db_name,
        username=SecretEnv.username,
        password=SecretEnv.password,
        port=SecretEnv.port,
        host=SecretEnv.host,
        declarative_base=DeclarativeBase
    )

    repository = PostgresRepository(connection)
    bot_scheduler = BotScheduler(repository)
    await bot_scheduler.start()

    print("okay!")
    # loop = asyncio.get_event_loop()
    # await loop.create_future()


if __name__ == '__main__':
    asyncio.run(main())
