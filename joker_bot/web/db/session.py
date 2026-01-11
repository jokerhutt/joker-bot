from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .engine import get_engine

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal(bind=get_engine()) as session:
        yield session
