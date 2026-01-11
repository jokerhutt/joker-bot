from platform import java_ver
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, or_, select
from joker_bot.web.models.user_stats import UserStats
from joker_bot.web.models.transaction import Transaction


async def get_user_transactions(
    session: AsyncSession,
    discord_id: int,
    limit: int | None = None,
) -> list[Transaction]:
    stmt = (
        select(Transaction)
        .where(
            or_(
                Transaction.sender_id == discord_id,
                Transaction.receiver_id == discord_id,
            )
        )
        .order_by(Transaction.created_at.desc())
    )

    if limit is not None:
        stmt = stmt.limit(limit)

    result = await session.execute(stmt)
    return list(result.scalars().all())


async def create_transaction(
    session: AsyncSession,
    sender_id: int,
    sender_username: str,
    receiver_id: int,
    receiver_username: str,
    amount: int,
) -> Transaction:
    transaction = Transaction(
        sender_id=sender_id,
        sender_username=sender_username,
        receiver_id=receiver_id,
        receiver_username=receiver_username,
        amount=amount,
    )
    session.add(transaction)
    return transaction
