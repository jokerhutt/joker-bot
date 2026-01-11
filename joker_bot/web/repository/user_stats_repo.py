from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from joker_bot.web.models.user_stats import UserStats


async def get_or_create_user_stats(
    session: AsyncSession,
    discord_id: int,
) -> UserStats:
    stats = await session.get(UserStats, discord_id)
    if stats is not None:
        return stats

    stats = UserStats(
        discord_id=discord_id,
        balance=0,
    )
    session.add(stats)

    try:
        await session.flush()
        return stats

    except IntegrityError:
        await session.rollback()
        stats = await session.get(UserStats, discord_id)
        if stats is None:
            raise RuntimeError("UserStats upsert failed unexpectedly")
        return stats


async def update_points(
    session: AsyncSession,
    discord_id: int,
    delta: int,
) -> None:
    stats = await session.get(UserStats, discord_id)
    if stats:
        stats.balance += delta
