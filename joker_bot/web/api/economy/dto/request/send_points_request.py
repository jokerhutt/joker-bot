from pydantic import BaseModel, Field


class SendPointsRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: int = Field(gt=0)
