import hikari
import lightbulb
import logging

from joker_bot.bot.economy.client.economy_client import EconomyClient

plugin = lightbulb.Plugin("economy")


@plugin.command
@lightbulb.command("economy", "Economy-related commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def economy_group() -> None:
    """Economy command group."""
    pass


@economy_group.child
@lightbulb.command("balance", "Check your balance")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def balance_command(ctx: lightbulb.Context) -> None:
    client: EconomyClient = ctx.bot.d["economy_client"]

    try:
        balance: int = await client.get_balance(ctx.user.id)

        await ctx.respond(
            f"You have **{balance}** points.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

    except Exception:
        await ctx.respond(
            "Failed to fetch balance.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
