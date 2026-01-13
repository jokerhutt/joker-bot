from datetime import datetime
from typing import TypedDict, List, Optional


class MessageDTO(TypedDict):
    id: str
    author_id: str
    content: str | None
    timestamp: str


class ChatBatchDTO(TypedDict):
    channel_id: str
    messages: list[MessageDTO]


class ChatMessageInsert(TypedDict):
    id: str
    channel_id: str
    guild_id: str | None
    author_id: str
    content: str | None
    created_at: datetime
