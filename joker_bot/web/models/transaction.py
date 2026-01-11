from datetime import datetime
import uuid
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from joker_bot.web.models.base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    sender_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL")
    )

    sender_username: Mapped[str] = mapped_column(String)

    receiver_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL")
    )

    description: Mapped[str | None] = mapped_column(String, nullable=True)

    receiver_username: Mapped[str] = mapped_column(String)

    amount: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
