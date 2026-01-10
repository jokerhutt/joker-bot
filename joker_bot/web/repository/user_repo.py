from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from joker_bot.web.models.user import User
from joker_bot.web.models.user_stats import UserStats


async def get_or_create_user(
    session: AsyncSession,
    discord_id: int,
) -> User:
    user = await session.get(User, discord_id)
    if user is not None:
        return user

    user = User(discord_user_id=discord_id)
    session.add(user)

    try:
        await session.flush()
        return user
    except IntegrityError:
        await session.rollback()
        user = await session.get(User, discord_id)
        if user is None:
            raise RuntimeError("User upsert failed unexpectedly")
        return user
