from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from joker_bot.web.api.economy.dto.request.send_points_request import SendPointsRequest
from joker_bot.web.api.economy.dto.response.balance_response import BalanceResponse
from joker_bot.web.db.session import get_session
from joker_bot.web.service.economy_service import BadRequestException, UserStatsService


router = APIRouter(prefix="/economy")


@router.post("/send")
async def send_points(
    body: SendPointsRequest,
    session=Depends(get_session),
):
    _ = await UserStatsService().send_points(
        session,
        body.sender_id,
        body.receiver_id,
        body.amount,
    )
    return {"ok": True}


@router.get("/balance/{discord_id}")
async def get_balance(
    discord_id: int,
    session: AsyncSession = Depends(get_session),
) -> BalanceResponse:
    try:
        balance = await UserStatsService().get_balance(session, discord_id)
        return BalanceResponse(discord_id=discord_id, balance=balance)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
