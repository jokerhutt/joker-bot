from fastapi import APIRouter, Depends

from joker_bot.web.api.economy.dto.request.send_points_request import SendPointsRequest
from joker_bot.web.service.economy_service import UserStatsService


router = APIRouter(prefix="/economy")


@router.post("/send")
async def send_points(
    body: SendPointsRequest,
    session=Depends(get_session),
):
    await UserStatsService().send_points(
        session,
        body.sender_id,
        body.receiver_id,
        body.amount,
    )
    return {"ok": True}
