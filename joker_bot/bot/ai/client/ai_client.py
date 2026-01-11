from joker_bot.bot.api_client import APIClient


class AiClient:
    def __init__(self, api: APIClient):
        self._api = api

    async def send_prompt(
        self,
        discord_id: int,
        username: str,
        user_message: str,
        recent_messages: list[tuple[str, str]],
    ) -> str:
        resp = await self._api.post(
            "/ai/prompt",
            json={
                "discord_id": discord_id,
                "username": username,
                "user_message": user_message,
                "recent_messages": recent_messages,
            },
        )
        return resp
