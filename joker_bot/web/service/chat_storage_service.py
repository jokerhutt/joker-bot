from datetime import datetime
import json
from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.api.chat_storage.dto.message_dto import (
    ChatBatchDTO,
    ChatMessageInsert,
)
from joker_bot.web.repository.chat_message_repo import save_chat_messages
from joker_bot.web.service.base_service import BaseService


class ChatStorageService(BaseService):
    def __init__(self):
        super().__init__()

    async def persist_chat_messages(
        self,
        session: AsyncSession,
        batch: ChatBatchDTO,
    ) -> None:
        message_inserts: list[ChatMessageInsert] = []

        channel_id = batch["channel_id"]

        self.logger.info(f"Persist chat messages: Channel id = {channel_id}")

        for msg in batch["messages"]:
            message_inserts.append(
                {
                    "id": msg["id"],
                    "channel_id": channel_id,
                    "guild_id": None,
                    "author_id": msg["author_id"],
                    "content": msg["content"],
                    "created_at": datetime.fromisoformat(msg["timestamp"]),
                }
            )

            self.logger.info(f"Appended message insert: {json.dumps(msg)}")

        if not message_inserts:
            return

        await save_chat_messages(session, message_inserts)
