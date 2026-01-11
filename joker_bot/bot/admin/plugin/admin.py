import hikari
import lightbulb

from joker_bot.bot.admin.client.admin_client import AdminClient
from joker_bot.bot.hook.has_role import use_has_role

APPROVED_ROLES = "robot custodian"

plugin = lightbulb.Plugin("tag")

# -------- TAG GROUP --------


@plugin.command
@lightbulb.command("tag", "Bot administration commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def tag_group() -> None:
    pass


# -------- GET TAG --------


@tag_group.child
@lightbulb.option(
    "user",
    "User to inspect",
    type=hikari.User,
    required=True,
)
@lightbulb.command("get", "Get a user's tag")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_tag(ctx: lightbulb.Context) -> None:
    if not use_has_role(ctx, APPROVED_ROLES):
        await ctx.respond(
            f"You are not a **{APPROVED_ROLES}**.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    client: AdminClient = ctx.bot.d["admin_client"]
    target: hikari.User = ctx.options.user

    try:
        tag = await client.get_user_tag(target.id)

        await ctx.respond(
            f"**{target.username}** has tag: `{tag}`",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

    except Exception:
        await ctx.respond(
            "Failed to fetch user tag.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


# -------- SET TAG --------


@tag_group.child
@lightbulb.option(
    "user",
    "User to update",
    type=hikari.User,
    required=True,
)
@lightbulb.option(
    "tag",
    "New tag",
    type=str,
    required=True,
)
@lightbulb.command("set", "Set a user's tag")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_tag(ctx: lightbulb.Context) -> None:
    if not use_has_role(ctx, APPROVED_ROLES):
        await ctx.respond(
            f"You are not a **{APPROVED_ROLES}**.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    client: AdminClient = ctx.bot.d["admin_client"]
    target: hikari.User = ctx.options.user
    new_tag: str = ctx.options.tag

    try:
        await client.update_user_tag(
            discord_id=target.id,
            new_tag=new_tag,
        )

        await ctx.respond(
            f"Updated **{target.username}** tag to `{new_tag}`",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

    except Exception:
        await ctx.respond(
            "Failed to update user tag.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
