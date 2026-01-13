# joker_bot/bot/main.py
import os
import hikari
import lightbulb
from dotenv import load_dotenv

from joker_bot.bot.api_client import APIClient
from joker_bot.bot.economy.client.economy_client import EconomyClient
from joker_bot.bot.ai.client.ai_client import AiClient
from joker_bot.bot.admin.client.admin_client import AdminClient
from joker_bot.bot.collect.client.collect_client import ChatClient

load_dotenv()


def get_guild_ids() -> tuple[int, ...]:
    raw = os.getenv("GUILD_IDS")
    if not raw:
        return ()

    return tuple(int(gid.strip()) for gid in raw.split(",") if gid.strip())


def run() -> None:
    bot = lightbulb.BotApp(
        token=os.environ["DISCORD_TOKEN"],
        intents=hikari.Intents.ALL,
        default_enabled_guilds=get_guild_ids(),
        prefix="!",
    )

    api_client = APIClient(
        base_url=os.environ["API_BASE_URL"],
    )

    bot.d["custodian_roles"] = {
        r.strip().lower()
        for r in os.getenv("CUSTODIAN_ROLES", "").split(",")
        if r.strip()
    }

    bot.d["tech_roles"] = {
        r.strip().lower() for r in os.getenv("TECH_ROLES", "").split(",") if r.strip()
    }

    economy_client = EconomyClient(api_client)
    ai_client = AiClient(api_client)
    admin_client = AdminClient(api_client)
    chat_client = ChatClient(api_client)

    bot.d["economy_client"] = economy_client
    bot.d["ai_client"] = ai_client
    bot.d["admin_client"] = admin_client
    bot.d["chat_client"] = chat_client

    bot.load_extensions(
        "joker_bot.bot.economy.plugin.economy",
        "joker_bot.bot.ai.plugin.ai",
        "joker_bot.bot.admin.plugin.admin",
        "joker_bot.bot.collect.plugin.collect",
    )

    bot.run()


if __name__ == "__main__":
    run()
