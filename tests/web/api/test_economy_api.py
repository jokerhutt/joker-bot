import pytest

from joker_bot.web.models.user import User


@pytest.mark.asyncio
async def test_get_balance_creates_user_and_stats(api_client, session):
    user = User(id=123)
    session.add(user)
    await session.commit()

    # Act
    response = await api_client.get("/economy/balance/123")

    # Assert HTTP
    assert response.status_code == 200
    body = response.json()

    assert body["discord_id"] == 123
    assert body["balance"] == 0
