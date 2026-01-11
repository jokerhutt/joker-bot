from __future__ import annotations

import httpx
from typing import Any


from typing import Any

from joker_bot.bot.api_client import APIClient


class EconomyClient:
    def __init__(self, api: APIClient):
        self._api = api

    # -------- balance --------

    async def get_balance(self, discord_id: int) -> int:
        data = await self._api.get(f"/economy/balance/{discord_id}")
        return data["balance"]

    # -------- transfers --------

    async def send_points(
        self,
        sender_id: int,
        receiver_id: int,
        amount: int,
    ) -> None:
        await self._api.post(
            "/economy/send",
            json={
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "amount": amount,
            },
        )

    # -------- history --------

    async def get_transaction_history(
        self,
        discord_id: int,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        data = await self._api.get(
            f"/economy/transactions/{discord_id}",
            params={"limit": limit},
        )
        return data
