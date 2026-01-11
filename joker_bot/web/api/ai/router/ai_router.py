from fastapi import APIRouter, Depends

from joker_bot.web.api.ai.dto.request.ai_message_request import AiMessageRequest
from joker_bot.web.db.session import get_session
from joker_bot.web.service.ai_service import AiService


router = APIRouter(prefix="/ai")


@router.post("/prompt")
async def send_ai_prompt(body: AiMessageRequest, session=Depends(get_session)):
    response = await AiService().send_ai_message(
        session=session,
        discord_id=body.discord_id,
        username=body.username,
        user_message=body.user_message,
        recent_messages=body.recent_messages,
    )
    return response
