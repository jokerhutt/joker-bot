from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from joker_bot.web.models.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    channel_id: Mapped[str] = mapped_column(String, index=True, nullable=False)

    guild_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)

    author_id: Mapped[str] = mapped_column(String, index=True, nullable=False)

    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
