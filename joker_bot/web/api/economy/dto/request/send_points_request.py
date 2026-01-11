from pydantic import BaseModel, Field


class SendPointsRequest(BaseModel):
    sender_id: int
    sender_username: str
    receiver_id: int
    receiver_username: str
    amount: int = Field(gt=0)
