import lightbulb


def use_has_role(ctx: lightbulb.Context, role_name: str) -> bool:
    member = ctx.member
    if member is None:
        return False

    app = ctx.app

    for role_id in member.role_ids:
        role = app.cache.get_role(role_id)
        if role and role.name.lower() == role_name:
            return True

    return False
