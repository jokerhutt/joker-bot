from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from joker_bot.web.api.chat_storage.dto.message_dto import ChatMessageInsert
from joker_bot.web.models.chat_message import ChatMessage


async def save_chat_messages(
    session: AsyncSession,
    messages: list[ChatMessageInsert],
) -> None:
    if not messages:
        return

    stmt = (
        insert(ChatMessage)
        .values(messages)
        .on_conflict_do_nothing(index_elements=["id"])
    )

    await session.execute(stmt)
