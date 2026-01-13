from datetime import datetime, timezone
import pytest

from joker_bot.web.api.user.dto.request.user_tag_request import UserTagRequest
from joker_bot.web.models.user import User


from datetime import datetime, timezone
import pytest

from joker_bot.web.models.chat_message import ChatMessage


@pytest.mark.asyncio
async def test_upload_chat_history_returns_ok(api_client, session):
    payload = {
        "channel_id": "123456789",
        "messages": [
            {
                "id": "111",
                "author_id": "222",
                "content": "hello world",
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            },
            {
                "id": "112",
                "author_id": "223",
                "content": "second message",
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            },
        ],
    }

    response = await api_client.post(
        "/chat/save",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}

    messages = (await session.execute(ChatMessage.__table__.select())).fetchall()

    assert len(messages) == 2

    ids = {row.id for row in messages}
    assert ids == {"111", "112"}
