from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TransactionRole(Enum):
    SENDER = "Sender"
    RECEIVER = "Receiver"


class TransactionEntryResponse(BaseModel):
    sender_name: str
    receiver_name: str
    user_role: TransactionRole
    amount: int
    time: datetime
