from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from joker_bot.web.models.base import Base


class UserStats(Base):
    __tablename__ = "user_stats"

    discord_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )

    balance: Mapped[int] = mapped_column(default=0)
