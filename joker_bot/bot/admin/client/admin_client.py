from joker_bot.bot.api_client import APIClient


class AdminClient:
    def __init__(self, api: APIClient):
        self._api = api

    # -------- balance --------

    async def get_user_tag(self, discord_id: int) -> int:
        data = await self._api.get(f"/user/tag/{discord_id}")
        return data

    # -------- transfers --------

    async def update_user_tag(self, discord_id: int, new_tag: str) -> None:
        data = await self._api.post(
            "/user/tag",
            json={"discord_id": discord_id, "new_tag": new_tag},
        )
        return data
