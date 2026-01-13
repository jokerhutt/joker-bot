from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.api.chat_storage.dto.message_dto import ChatBatchDTO
from joker_bot.web.db.session import get_session
from joker_bot.web.service.chat_storage_service import ChatStorageService

router = APIRouter(prefix="/chat")


@router.post("/save")
async def persist_chat_history(
    body: ChatBatchDTO,
    session: AsyncSession = Depends(get_session),
):

    await ChatStorageService().persist_chat_messages(
        session=session,
        batch=body,
    )

    await session.commit()
    return {"ok": True}
