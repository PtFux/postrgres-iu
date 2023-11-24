from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class BaseRepository:

    def __init__(self, connection_setting, echo_logs=False):
        self._async_session = None
        self._username = connection_setting.username
        self._port = connection_setting.port
        self._host = connection_setting.host
        self._db_name = connection_setting.db_name
        self._password = connection_setting.password
        self._declarative_base = connection_setting.declarative_base

        self._echo_logs = echo_logs
        self._engine = None

        self._is_init = False

    async def initialize(self):

        engine = create_async_engine(
            f"postgresql+asyncpg://"
            f"{self._username}:{self._password}"
            f"@{self._host}:{self._port}"
            f"/{self._db_name}",
            echo=self._echo_logs
        )

        async with engine.begin() as conn:
            await conn.run_sync(self._declarative_base.metadata.create_all)

        self._async_session = async_sessionmaker(engine, expire_on_commit=False)
        self._is_init = True

    def _check_init(self):
        if not self._is_init:
            raise Exception(f"'Repository' not initialized")

    async def _select_one(self, stmt) -> Any:
        self._check_init()

        async with self._async_session() as session:
            async with session.begin():
                session: AsyncSession
                result = await session.execute(stmt)
                return result.scalar_one_or_none()

    async def _select_many(self, stmt) -> Any:
        self._check_init()

        async with self._async_session() as session:
            async with session.begin():
                session: AsyncSession
                result = await session.execute(stmt)
                return result.all()

    async def _query_without_result(self, stmt) -> None:
        self._check_init()

        async with self._async_session() as session:
            async with session.begin():
                session: AsyncSession
                await session.execute(stmt)

    async def _insert_one(self, entity):
        self._check_init()

        async with self._async_session() as session:
            async with session.begin():
                session: AsyncSession
                session.add(entity)
                await session.commit()

    async def _insert_many(self, entities):
        self._check_init()

        async with self._async_session() as session:
            async with session.begin():
                session: AsyncSession
                session.add_all(entities)
                await session.commit()
