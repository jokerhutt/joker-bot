# tests/conftest.py

import pytest_asyncio
from typing import AsyncGenerator
import pytest
import asyncio
from sqlalchemy import NullPool, make_url
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.engine import URL

from joker_bot.web.models.base import Base
from joker_bot.web.models import user, user_stats, transaction


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------- PostgreSQL container ----------


@pytest_asyncio.fixture(scope="session")
async def postgres_container() -> AsyncGenerator[PostgresContainer, None]:
    container = PostgresContainer("postgres:16")
    container.start()
    try:
        yield container
    finally:
        container.stop()


# ---------- Async engine ----------


@pytest_asyncio.fixture(scope="session")
async def async_engine(postgres_container):
    url = make_url(postgres_container.get_connection_url())
    url = url.set(drivername="postgresql+asyncpg")

    engine = create_async_engine(
        url,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


# ---------- DB session ----------


@pytest_asyncio.fixture
async def session(
    async_engine,
) -> AsyncGenerator[AsyncSession, None]:
    SessionFactory = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
    )

    async with SessionFactory() as session:
        yield session
        await session.rollback()
