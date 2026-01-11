# joker_bot/bot/main.py
import os
import hikari
import lightbulb
from dotenv import load_dotenv

from joker_bot.bot.api_client import APIClient
from joker_bot.bot.economy.client.economy_client import EconomyClient

load_dotenv()


def run() -> None:
    bot = lightbulb.BotApp(
        token=os.environ["DISCORD_TOKEN"],
        intents=hikari.Intents.ALL,
    )

    api_client = APIClient(
        base_url=os.environ["API_BASE_URL"],
    )

    economy_client = EconomyClient(api_client)

    bot.d["economy_client"] = economy_client

    bot.load_extensions(
        "joker_bot.bot.economy.plugin.economy",
    )

    bot.run()


if __name__ == "__main__":
    run()
