from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from joker_bot.web.models.user import User
from joker_bot.web.models.user_stats import UserStats


async def get_or_create_user(
    session: AsyncSession, discord_id: int, username: str | None = None
) -> User:
    user = await session.get(User, discord_id)
    if user is not None:
        return user

    user = User(id=discord_id, username=username)
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


async def set_user_tag(
    session: AsyncSession,
    discord_id: int,
    new_tag: str,
) -> User:
    user = await get_or_create_user(session, discord_id)

    user.tag = new_tag

    await session.flush()

    return user
