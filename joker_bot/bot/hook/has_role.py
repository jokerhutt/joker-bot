from collections.abc import Iterable
import lightbulb


def use_has_role(
    ctx: lightbulb.Context,
    role_names: Iterable[str],
) -> bool:
    member = ctx.member
    if member is None:
        return False

    app = ctx.app

    # normalize once
    wanted = {name.lower() for name in role_names}

    for role_id in member.role_ids:
        role = app.cache.get_role(role_id)
        if role and role.name.lower() in wanted:
            return True

    return False
