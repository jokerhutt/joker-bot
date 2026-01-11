from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.models.transaction import Transaction
from joker_bot.web.repository.transaction_repo import create_transaction
from joker_bot.web.repository.user_repo import get_or_create_user
from joker_bot.web.repository.user_stats_repo import get_or_create_user_stats


class InsufficientBalanceError(Exception):
    pass


class BadRequestException(Exception):
    pass


class UserStatsService:
    async def get_balance(
        self,
        session: AsyncSession,
        discord_id: int,
    ) -> int:
        await get_or_create_user(session, discord_id)
        stats = await get_or_create_user_stats(session, discord_id)
        return stats.balance

    async def send_points(
        self, session: AsyncSession, sender_id: int, receiver_id: int, amount: int
    ) -> int:
        sender_balance = await self.get_balance(session, sender_id)
        receiver_balance = await self.get_balance(session, receiver_id)

        if amount < 0:
            raise BadRequestException(f"You must send a positive integer")

        if sender_balance < amount:
            raise InsufficientBalanceError(
                f"User {sender_id} has {sender_balance}, needs {amount}"
            )

        transaction: Transaction = await create_transaction(
            session, sender_id, receiver_id, amount
        )
        return transaction.amount
