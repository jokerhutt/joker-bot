import lightbulb


def use_has_role(ctx: lightbulb.Context, role_names: set[str]) -> bool:
    member = ctx.member
    if member is None:
        return False

    for role_id in member.role_ids:
        role = ctx.app.cache.get_role(role_id)
        if not role:
            continue

        if role.name.lower() in role_names:
            return True

    return False
