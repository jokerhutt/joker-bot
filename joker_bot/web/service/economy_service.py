from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.api.economy.dto.response.transaction_history import (
    TransactionEntryResponse,
    TransactionRole,
)
from joker_bot.web.models.transaction import Transaction
from joker_bot.web.repository.transaction_repo import (
    create_transaction,
    get_user_transactions,
)
from joker_bot.web.repository.user_repo import get_or_create_user
from joker_bot.web.repository.user_stats_repo import get_or_create_user_stats


class InsufficientBalanceError(Exception):
    pass


class BadRequestException(Exception):
    pass


class EconomyService:

    def decide_role(self, user_id: int, sender_id: int) -> TransactionRole:
        if user_id == sender_id:
            return TransactionRole.SENDER
        else:
            return TransactionRole.RECEIVER

    async def get_balance(
        self,
        session: AsyncSession,
        discord_id: int,
    ) -> int:
        _ = await get_or_create_user(session, discord_id)
        stats = await get_or_create_user_stats(session, discord_id)
        return stats.balance

    async def get_transaction_history(
        self, session: AsyncSession, discord_id: int, limit: int = 10
    ):
        _ = await get_or_create_user(session, discord_id)
        transactions: list[Transaction] = await get_user_transactions(
            session, discord_id, limit
        )

        transactionEntries: list[TransactionEntryResponse] = []

        for transaction in transactions:
            transactionEntries.append(
                TransactionEntryResponse(
                    sender_name=transaction.sender_username,
                    receiver_name=transaction.receiver_username,
                    user_role=self.decide_role(discord_id, transaction.sender_id),
                    amount=transaction.amount,
                    time=transaction.created_at,
                )
            )

        return transactionEntries

    async def send_points(
        self,
        session: AsyncSession,
        sender_id: int,
        sender_username: str,
        receiver_id: int,
        receiver_username: str,
        amount: int,
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
            session,
            sender_id=sender_id,
            sender_username=sender_username,
            receiver_id=receiver_id,
            receiver_username=receiver_username,
            amount=amount,
        )
        return transaction.amount
