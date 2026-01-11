from hikari import TextableChannel


class ChatService:
    async def use_recent_messages(
        self,
        channel: TextableChannel,
        limit: int = 20,
    ) -> list[tuple[str, str]]:
        messages: list[tuple[str, str]] = []

        async for msg in channel.fetch_history():
            if msg.author is None:
                continue
            if msg.author.is_bot:
                continue
            if not msg.content:
                continue

            messages.append((msg.author.username, msg.content))

            if len(messages) >= limit:
                break

        return messages[::-1]
