import logging
import hikari
import lightbulb

from joker_bot.bot.admin.client.admin_client import AdminClient
from joker_bot.bot.hook.has_role import use_has_role

plugin = lightbulb.Plugin("tag")
logger = logging.getLogger(__name__)
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
    approved_roles: set[str] = ctx.bot.d["custodian_roles"]
    member = ctx.member
    user_roles: list[str] = []
    if member is not None:
        for role_id in member.role_ids:
            role = ctx.app.cache.get_role(role_id)
            if role:
                user_roles.append(role.name)

    logger.info(
        "Admin command check | user=%s (%s) | user_roles=%s | approved_roles=%s",
        ctx.user.username,
        ctx.user.id,
        user_roles,
        list(approved_roles),
    )

    if not use_has_role(ctx, approved_roles):
        logger.warning(
            "Permission denied | user=%s (%s)",
            ctx.user.username,
            ctx.user.id,
        )
        await ctx.respond(
            "You are not **approved**.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if not use_has_role(ctx, approved_roles):
        await ctx.respond(
            f"You are not **approved**.",
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
    approved_roles: set[str] = ctx.bot.d["custodian_roles"]
    if not use_has_role(ctx, approved_roles):
        await ctx.respond(
            f"You are not a **{approved_roles}**.",
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
