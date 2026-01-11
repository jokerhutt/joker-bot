import pytest

from joker_bot.web.models.user import User
from joker_bot.web.repository.user_stats_repo import (
    get_or_create_user_stats,
    update_points,
)


@pytest.mark.asyncio
async def test_create_and_get_user_stats(session):
    # FK prerequisite
    user = User(id=123)
    session.add(user)
    await session.commit()

    await get_or_create_user_stats(session, discord_id=123)
    await session.commit()

    stats = await get_or_create_user_stats(session, 123)

    assert stats is not None
    assert stats.discord_id == 123
    assert stats.balance == 0


@pytest.mark.asyncio
async def test_update_points(session):
    user = User(id=456)
    session.add(user)
    await session.commit()

    await get_or_create_user_stats(session, discord_id=456)
    await session.commit()

    await update_points(session, 456, 10)
    await session.commit()

    stats = await get_or_create_user_stats(session, 456)

    assert stats is not None
    assert stats.balance == 10
