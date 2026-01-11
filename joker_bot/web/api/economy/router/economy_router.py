from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from joker_bot.web.api.economy.dto.request.send_points_request import SendPointsRequest
from joker_bot.web.api.economy.dto.response.balance_response import BalanceResponse
from joker_bot.web.api.economy.dto.response.transaction_history import (
    TransactionEntryResponse,
)
from joker_bot.web.db.session import get_session
from joker_bot.web.service.economy_service import (
    BadRequestException,
    InsufficientBalanceError,
    EconomyService,
)

router = APIRouter(prefix="/economy")


@router.post("/send")
async def send_points(
    body: SendPointsRequest,
    session=Depends(get_session),
):
    try:
        _ = await EconomyService().send_points(
            session,
            body.sender_id,
            body.sender_username,
            body.receiver_id,
            body.receiver_username,
            body.amount,
        )
        return {"ok": True}

    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InsufficientBalanceError as e:
        raise InsufficientBalanceError("Insufficient Balance")


@router.get("/balance/{discord_id}")
async def get_balance(
    discord_id: int,
    session: AsyncSession = Depends(get_session),
) -> BalanceResponse:
    balance = await EconomyService().get_balance(session, discord_id)
    return BalanceResponse(discord_id=discord_id, balance=balance)


@router.get("/transactions/{discord_id}")
async def get_transactions(
    discord_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[TransactionEntryResponse]:
    transactions = await EconomyService().get_transaction_history(
        session=session, discord_id=discord_id
    )
    return transactions
