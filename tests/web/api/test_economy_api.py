from datetime import datetime, timezone
import pytest

from joker_bot.web.models.transaction import Transaction
from joker_bot.web.models.user import User


@pytest.mark.asyncio
async def test_get_balance_creates_user_and_stats(api_client, session):
    user = User(id=123, username="John")
    session.add(user)
    await session.commit()

    # Act
    response = await api_client.get("/economy/balance/123")

    # Assert HTTP
    assert response.status_code == 200
    body = response.json()

    assert body["discord_id"] == 123
    assert body["balance"] == 100


@pytest.mark.asyncio
async def test_get_transaction_history_returns_transaction_history(api_client, session):
    user = User(id=123, username="John")
    user_2 = User(id=124, username="Steve")

    session.add(user)
    session.add(user_2)

    await session.commit()

    user_1_stats = await api_client.get("/economy/balance/123")
    user_2_stats = await api_client.get("/economy/balance/124")

    transaction_1 = Transaction(
        sender_id=user.id,
        receiver_id=user_2.id,
        sender_username="John",
        receiver_username="Steve",
        amount=10,
        created_at=datetime.now(timezone.utc),
    )

    transaction_2 = Transaction(
        sender_id=user.id,
        receiver_id=user_2.id,
        sender_username="John",
        receiver_username="Steve",
        amount=10,
        created_at=datetime.now(timezone.utc),
    )

    transaction_3 = Transaction(
        sender_id=user_2.id,
        receiver_id=user.id,
        sender_username="Steve",
        receiver_username="John",
        amount=10,
        created_at=datetime.now(timezone.utc),
    )

    session.add(transaction_1)
    session.add(transaction_2)
    session.add(transaction_3)

    await session.commit()

    response = await api_client.get("/economy/transactions/123")

    assert response.status_code == 200
    body = response.json()

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 3

    assert body[0]["amount"] == 10
    assert body[0]["sender_name"] == "Steve"
    for tx in body:
        if tx["sender_name"] == "John":
            assert tx["user_role"] == "Sender"
        else:
            assert tx["user_role"] == "Receiver"
