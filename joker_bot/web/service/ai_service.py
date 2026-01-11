from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.api.app import AI_SYSTEM_INSTRUCTION
from joker_bot.web.repository.user_repo import get_or_create_user
from joker_bot.web.service.base_service import BaseService


class AiService(BaseService):

    async def get_custom_user_prompt(
        self, session: AsyncSession, discord_id: int, username: str
    ) -> str:
        user = await get_or_create_user(session, discord_id=discord_id)
        tag = user.tag

        if user.tag:
            return (
                f"The following instruction has higher priority than previous behavior rules:\n"
                f"You must act as: {user.tag}\n"
                f"Only override traits that directly conflict with this instruction."
            )
        return ""

    async def build_prompt(self, session: AsyncSession, discord_id: int, username: str, user_message: str)
        main_instruction = AI_SYSTEM_INSTRUCTION
        user_override_instruction = await self.get_custom_user_prompt(session, discord_id=discord_id, username=username)
        
        prompt_parts = [
            "### SYSTEM INSTRUCTION (base persona)",
            main_instruction.strip(),
        ]

        if user_override_instruction:
            prompt_parts.extend([
                "",
                "### USER OVERRIDE (higher priority)",
                user_override.strip(),
            ])

        prompt_parts.extend([
            "",
            "### USER MESSAGE",
            user_message.strip(),
        ])

        return "\n".join(prompt_parts)
