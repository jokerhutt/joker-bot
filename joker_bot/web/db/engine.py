import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global _engine

    if _engine is None:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL is not set")

        _engine = create_async_engine(
            database_url,
            echo=False,
        )

    return _engine
