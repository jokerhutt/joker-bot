from pydantic import BaseModel


class BalanceResponse(BaseModel):
    discord_id: int
    balance: int
