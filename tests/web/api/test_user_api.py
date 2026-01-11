from datetime import datetime, timezone
import pytest

from joker_bot.web.api.user.dto.request.user_tag_request import UserTagRequest
from joker_bot.web.models.user import User


@pytest.mark.asyncio
async def test_get_tag_returns_user_tag(api_client, session):
    user = User(id=123, username="John", tag="Friendly")
    session.add(user)
    await session.commit()

    # Act
    response = await api_client.get(f"/user/tag/{user.id}")

    # Assert HTTP
    assert response.status_code == 200
    body = response.json()

    assert body == "Friendly"


@pytest.mark.asyncio
async def test_update_tag_returns_updated_user_tag(api_client, session):
    user = User(id=123, username="John", tag="Friendly")
    session.add(user)
    await session.commit()

    payload = {
        "discord_id": user.id,
        "new_tag": "Mean",
    }

    response = await api_client.post(
        "/user/tag",
        json=payload,
    )

    assert response.status_code == 200
    body = response.json()

    assert body == "Mean"
