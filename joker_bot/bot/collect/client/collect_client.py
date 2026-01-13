from joker_bot.bot.api_client import APIClient
from joker_bot.web.api.chat_storage.dto.message_dto import ChatBatchDTO


class ChatClient:
    def __init__(self, api: APIClient):
        self._api = api

    async def save_chat_batch(self, chat_batch: ChatBatchDTO) -> None:
        payload = {
            "channel_id": chat_batch["channel_id"],
            "messages": [
                {
                    "id": m["id"],
                    "author_id": m["author_id"],
                    "content": m["content"],
                    "timestamp": m["timestamp"],
                }
                for m in chat_batch["messages"]
            ],
        }

        await self._api.post("/chat/save", json=payload)
