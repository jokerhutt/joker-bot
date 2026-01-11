from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.models.user import User
from joker_bot.web.repository.user_repo import get_or_create_user, set_user_tag
from joker_bot.web.service.base_service import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__()

    async def get_tag(self, session: AsyncSession, discord_id: int) -> str:
        user = await get_or_create_user(session=session, discord_id=discord_id)
        if user.tag:
            return user.tag
        else:
            return "No Tag"

    async def set_tag(
        self, session: AsyncSession, discord_id: int, new_tag: str
    ) -> str:
        user = await get_or_create_user(session, discord_id)

        if user.tag is None:
            raise RuntimeError(f"User {discord_id} has no tag set")

        return user.tag
