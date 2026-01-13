import json
import logging
import lightbulb
from typing import cast

from hikari.channels import TextableChannel
from joker_bot.bot.collect.client.collect_client import ChatClient
from joker_bot.bot.hook.has_role import use_has_role
from joker_bot.web.api.chat_storage.dto.message_dto import ChatBatchDTO, MessageDTO

plugin = lightbulb.Plugin("chat")
logger = logging.getLogger(__name__)


@lightbulb.command("pingu", "Collect messages in chat (WIP)")
@lightbulb.implements(lightbulb.PrefixCommand)
async def collect_history(ctx: lightbulb.PrefixContext) -> None:
    approved_roles: set[str] = ctx.bot.d["tech_roles"]

    if not use_has_role(ctx, approved_roles):
        await ctx.respond("You are not **approved**.")
        return

    client: ChatClient = ctx.bot.d["chat_client"]

    channel = ctx.app.cache.get_guild_channel(ctx.channel_id)
    if channel is None:
        await ctx.respond("This command must be used in a guild text channel.")
        return

    channel = cast(TextableChannel, cast(object, channel))

    await ctx.respond("Starting message collection…")

    batch_messages: list[MessageDTO] = []
    batch_size = 100
    total = 0

    async for msg in channel.fetch_history():

        logger.info(f"Scanning message {total + 1}")

        if msg.author is None:
            logger.info(f"Msg has no author: {msg.id}")
            continue
        if msg.author.is_bot:
            logger.info(f"Msg has is bot: {msg.id}")
            continue
        if not msg.content:
            logger.info(f"Msg has no content: {msg.id}")
            continue

        message_to_append: MessageDTO = {
            "id": str(msg.id),
            "author_id": str(msg.author.id),
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
        }

        batch_messages.append(message_to_append)
        total += 1

        logger.info(f"Message appended: {json.dumps(message_to_append)}")

        if len(batch_messages) >= batch_size:
            batch: ChatBatchDTO = {
                "channel_id": str(channel.id),
                "messages": batch_messages,
            }

            await client.save_chat_batch(batch)
            batch_messages.clear()

        if total % 1000 == 0:
            _ = await ctx.respond(f"Pong: {total}")

    if batch_messages:
        batch: ChatBatchDTO = {
            "channel_id": str(channel.id),
            "messages": batch_messages,
        }
        await client.save_chat_batch(batch)

    _ = await ctx.respond(f"Pong Pong: {total}")
