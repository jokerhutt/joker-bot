from pydantic import BaseModel, Field


class AiMessageRequest(BaseModel):
    discord_id: int
    username: str
    user_message: str
    recent_messages: list[tuple[str, str]]
