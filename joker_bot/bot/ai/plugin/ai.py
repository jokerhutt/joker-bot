from collections.abc import Mapping
import hikari
import lightbulb

from joker_bot.bot.ai.client.ai_client import AiClient
from joker_bot.bot.hook.chat_history import ChatService

plugin = lightbulb.Plugin("ai")


@plugin.listener(hikari.MessageCreateEvent)
async def on_mention(event: hikari.MessageCreateEvent) -> None:
    # ---- basic guards ----
    if event.author is None or event.author.is_bot:
        return
    if not event.content:
        return

    bot = plugin.app
    me = bot.get_me()
    if me is None:
        return

    referenced = event.message.referenced_message
    is_replying_to_me = check_if_replying_to_me(referenced, me)

    # ---- mention check (typed) ----
    mentions: Mapping[hikari.Snowflake, hikari.User] = event.message.user_mentions or {}

    if me.id not in mentions:
        return

    # ---- fetch channel from cache ----
    channel = bot.cache.get_guild_channel(event.channel_id)
    if channel is None:
        return
    if not isinstance(channel, hikari.TextableChannel):
        return

    ai_client: AiClient = bot.d["ai_client"]

    # ---- strip mention ----
    user_message = (
        event.content.replace(f"<@{me.id}>", "").replace(f"<@!{me.id}>", "").strip()
    )
    if not user_message:
        return

    # ---- fetch history ----
    history = await ChatService().use_recent_messages(channel, limit=20)

    # ---- call AI ----
    response: str = await ai_client.send_prompt(
        discord_id=event.author.id,
        username=event.author.username,
        user_message=user_message,
        recent_messages=history,
    )

    await channel.send(response)


def check_if_replying_to_me(
    referenced: hikari.PartialMessage | None,
    me: hikari.OwnUser | None,
) -> bool:
    if referenced is None or me is None:
        return False

    author = referenced.author
    if isinstance(author, hikari.User):
        return author.id == me.id

    return False


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
