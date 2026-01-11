from sqlalchemy.ext.asyncio import AsyncSession
from joker_bot.web.api.app import AI_SYSTEM_INSTRUCTION
from joker_bot.web.client.gemini_client import generate_ai_response
from joker_bot.web.repository.user_repo import get_or_create_user
from joker_bot.web.service.base_service import BaseService


class AiService(BaseService):

    def __init__(self):
        super().__init__()

    async def send_ai_message(
        self,
        session: AsyncSession,
        discord_id: int,
        username: str,
        user_message: str,
        recent_messages: list[tuple[str, str]],
    ) -> str:
        full_prompt = await self.build_prompt(
            session, discord_id, username, user_message, recent_messages
        )

        resp = await generate_ai_response(full_prompt)
        if not resp or not resp.candidates:
            return "No response generated."

        candidate = resp.candidates[0]
        content = candidate.content
        if content is None or not content.parts:
            return "Empty response."

        return content.parts[0].text or ""

    async def get_custom_user_prompt(
        self, session: AsyncSession, discord_id: int
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

    async def build_prompt(
        self,
        session: AsyncSession,
        discord_id: int,
        username: str,
        user_message: str,
        recent_messages: list[tuple[str, str]] = [],
    ):
        main_instruction = AI_SYSTEM_INSTRUCTION
        user_override_instruction = await self.get_custom_user_prompt(
            session, discord_id=discord_id
        )

        prompt_parts = [
            "### SYSTEM INSTRUCTION (base persona)",
            main_instruction.strip(),
        ]

        if user_override_instruction:
            prompt_parts.extend(
                [
                    "",
                    "### USER OVERRIDE (higher priority)",
                    user_override_instruction.strip(),
                ]
            )

        if recent_messages:
            prompt_parts.append("")
            prompt_parts.append("### RECENT CONVERSATION")

            for author, content in recent_messages:
                prompt_parts.append(f"{author}: {content}")

        prompt_parts.extend(
            [
                "",
                "### USER MESSAGE",
                user_message.strip(),
            ]
        )

        return "\n".join(prompt_parts)
