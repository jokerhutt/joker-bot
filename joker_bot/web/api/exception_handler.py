from starlette.responses import JSONResponse

from joker_bot.web.service.economy_service import InsufficientBalanceError


@app.exception_handler(InsufficientBalanceError)
async def insufficient_balance_handler(_, exc):
    return JSONResponse(status_code=409, content={"detail": str(exc)})
