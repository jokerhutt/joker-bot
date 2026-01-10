from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from joker_bot.web.models.user_stats import UserStats


async def get_user_stats(
    session: AsyncSession,
    discord_id: int,
) -> UserStats | None:
    return await session.get(UserStats, discord_id)


async def create_user_stats(
    session: AsyncSession,
    discord_id: int,
) -> UserStats:
    stats = UserStats(
        discord_id=discord_id,
        balance=0,
    )
    session.add(stats)
    return stats


async def update_points(
    session: AsyncSession,
    discord_id: int,
    delta: int,
) -> None:
    stats = await session.get(UserStats, discord_id)
    if stats:
        stats.balance += delta
