from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from joker_bot.web.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, doc="Discord user ID (snowflake)"
    )

    tag: Mapped[str | None] = mapped_column(String, nullable=True)
